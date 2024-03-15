from pathlib import Path
from typing import Dict, Optional, Union

import anndata as ad
import bionty as bt
from lamin_utils import logger
from lamin_validator import AnnDataValidator
from lnschema_core.types import FieldAttr

from ._curate import convert_name_to_ontology_id
from ._fields import CellxGeneFields


def restrict_obs_fields(adata: ad.AnnData, obs_fields: Dict[str, FieldAttr]):
    """Restrict the obs fields so that there's no duplications."""
    obs_fields_unique = {k: v for k, v in obs_fields.items() if k in adata.obs.columns}
    for name, field in obs_fields.items():
        if name.endswith("_ontology_term_id"):
            continue
        # if both the ontology id and the name are present, only validate on the ontology_id
        if (
            name in adata.obs.columns
            and f"{name}_ontology_term_id" in adata.obs.columns
        ):
            obs_fields_unique.pop(name)
        # if the neither name nor ontology id are present, validate on the name
        # this will raise error downstream, we just use name to be more readable
        if (
            name not in adata.obs.columns
            and f"{name}_ontology_term_id" not in adata.obs.columns
        ):
            obs_fields_unique[name] = field
    return obs_fields_unique


def add_defaults_to_obs_fields(
    adata: ad.AnnData,
    **kwargs,
):
    """Add defaults to the obs fields."""
    added_defaults: Dict = {}
    for name, default in kwargs.items():
        if (
            name not in adata.obs.columns
            and f"{name}_ontology_term_id" not in adata.obs.columns
        ):
            adata.obs[name] = default
            added_defaults[name] = default
    if len(added_defaults) > 0:
        logger.important(f"added defaults to the AnnData object: {added_defaults}")


class Validator(AnnDataValidator):
    """CELLxGENE Lamin validator."""

    def __init__(
        self,
        adata: Union[ad.AnnData, str, Path],
        var_field: FieldAttr = bt.Gene.ensembl_gene_id,
        obs_fields: Dict[str, FieldAttr] = CellxGeneFields.OBS_FIELDS,
        using: str = "laminlabs/cellxgene",
        verbosity: str = "hint",
        **kwargs,
    ):
        add_defaults_to_obs_fields(adata, **kwargs)
        super().__init__(
            adata=adata,
            var_field=var_field,
            obs_fields=restrict_obs_fields(adata, obs_fields),
            using=using,
            verbosity=verbosity,
        )
        # TODO: deal with organism more consistently as other fields
        self._kwargs = {k: v for k, v in kwargs.items() if k == "organism"}

    @property
    def adata_curated(self) -> ad.AnnData:
        """Return the curated AnnData object."""
        return self._adata_curated

    def validate(self, **kwargs):
        """Validate the AnnData object."""
        # sets self._validated
        super().validate(**kwargs)
        return self._validated

    def register_labels(self, feature: str, validated_only: bool = True, **kwargs):
        """Register labels."""
        if feature == "all":
            for name in self.obs_fields.keys():
                logger.print(f"registering labels for feature '{name}'")
                super().register_labels(
                    feature=name, validated_only=validated_only, **kwargs
                )
        else:
            super().register_labels(
                feature=feature, validated_only=validated_only, **kwargs
            )

    def to_cellxgene(
        self, is_primary_data: bool, title: Optional[str] = None
    ) -> ad.AnnData:
        """Convert the AnnData object to cellxgene-schema input format."""
        # TODO: this should validate OBS_FIELDS
        if self._validated is None:
            raise ValueError("please first run `.validate()`!")
        adata_cxg = self._adata.copy()
        if "is_primary_data" not in adata_cxg.obs.columns:
            adata_cxg.obs["is_primary_data"] = is_primary_data
        # convert name column to ontology_term_id column
        for column in adata_cxg.obs.columns:
            if column in self.obs_fields and not column.endswith("_ontology_term_id"):
                mapped_column = convert_name_to_ontology_id(
                    adata_cxg.obs[column], field=self.obs_fields.get(column)
                )
                if mapped_column is not None:
                    adata_cxg.obs[f"{column}_ontology_term_id"] = mapped_column

        # drop the name columns for ontologies
        drop_columns = [
            i
            for i in adata_cxg.obs.columns
            if f"{i}_ontology_term_id" in adata_cxg.obs.columns
        ]
        adata_cxg.obs.drop(columns=drop_columns, inplace=True)
        if self._collection is None:
            if title is None:
                raise ValueError("please pass a title!")
            else:
                adata_cxg.uns["title"] = title
        else:
            adata_cxg.uns["title"] = self._collection.name
        return adata_cxg
