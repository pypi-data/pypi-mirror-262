from typing import Dict, Iterable, Optional

import lamindb as ln
import pandas as pd
from anndata import AnnData
from lamin_utils import colors, logger
from lamindb._from_values import _print_values
from lnschema_core import Registry
from lnschema_core.types import FieldAttr


def _registry_using(registry: Registry, using: Optional[str] = None) -> Registry:
    """Get a registry instance using a specific instance."""
    return (
        registry.using(using) if using is not None and using != "default" else registry
    )


def check_if_registry_needs_organism(
    registry: Registry, organism: Optional[str] = None
):
    """Check if a registry needs an organism."""
    if hasattr(registry, "organism_id"):
        if organism is None:
            raise ValueError(
                f"{registry.__name__} registry requires an organism!\n"
                "      → please pass an organism name via organism="
            )
        else:
            return True
    else:
        return False


def validate_categories_in_df(
    df: pd.DataFrame,
    fields: Dict[str, FieldAttr],
    using: Optional[str] = None,
    verbosity: str = "hint",
    **kwargs,
):
    """Validate categories in DataFrame columns using LaminDB registries."""
    former_verbosity = ln.settings.verbosity
    ln.settings.verbosity = verbosity

    def validate_categories(
        df: pd.DataFrame,
        feature_name: str,
        field: FieldAttr,
        using: Optional[str] = None,
        **kwargs,
    ):
        """Validate ontology terms in a pandas series using LaminDB registries."""
        values = df[feature_name].unique()
        registry = _registry_using(field.field.model, using)
        filter_kwargs = {}  # type: Dict[str, str]
        organism = kwargs.get("organism")
        if check_if_registry_needs_organism(registry, organism):
            filter_kwargs["organism"] = organism
        inspect_result = registry.inspect(
            values, field=field, mute=True, **filter_kwargs
        )
        # if all terms are validated
        n_non_validated = len(inspect_result.non_validated)
        if n_non_validated == 0:
            validated = True
            logger.success(f"all {feature_name}s are validated")
        else:
            are = "are" if n_non_validated > 1 else "is"
            print_values = _print_values(inspect_result.non_validated)
            feature_name_print = f"`.register_labels('{feature_name}')`"
            warning_message = (
                f"{colors.yellow(f'{n_non_validated} terms')} {are} not validated: "
                f"{colors.yellow(print_values)}\n      → register terms via "
                f"{colors.red(feature_name_print)}"
            )
            logger.warning(warning_message)
            validated = False
        return validated

    # start validation
    validated = True
    for feature_name, field in fields.items():
        logger.indent = ""
        logger.info(f"inspecting '{colors.bold(feature_name)}' by {field.field.name}")
        logger.indent = "   "
        validated &= validate_categories(
            df, feature_name=feature_name, field=field, using=using, **kwargs
        )
        logger.indent = ""

    ln.settings.verbosity = former_verbosity
    return validated


def validate_anndata(
    adata: AnnData,
    var_field: FieldAttr,
    obs_fields: Dict[str, FieldAttr],
    using: Optional[str] = None,
    verbosity: str = "hint",
    **kwargs,
) -> bool:
    """Inspect metadata in an AnnData object using LaminDB registries."""
    if using is not None and using != "default":
        logger.important(f"validating metadata using registries of instance `{using}`")

    validated_var = validate_features(
        adata.var.index,
        field=var_field,
        using=using,
        verbosity=verbosity,
        **kwargs,
    )
    validated_obs = validate_categories_in_df(
        adata.obs,
        fields=obs_fields,
        using=using,
        verbosity=verbosity,
        **kwargs,
    )
    return validated_var & validated_obs


def validate_features(
    values: Iterable[str],
    field: FieldAttr,
    using: Optional[str] = "default",
    verbosity: str = "hint",
    **kwargs,
):
    """Validate features using LaminDB registries."""
    former_verbosity = ln.settings.verbosity
    ln.settings.verbosity = verbosity
    model_field = f"{field.field.model.__name__}.{field.field.name}"
    logger.indent = ""
    logger.info(f"inspecting variables by {model_field}")
    logger.indent = "   "

    # inspect the values, validate and make suggestions to fix
    registry = _registry_using(field.field.model, using)
    filter_kwargs = {}  # type: Dict[str, str]
    organism = kwargs.get("organism")
    if check_if_registry_needs_organism(registry, organism):
        filter_kwargs["organism"] = organism
    inspect_result = registry.inspect(values, field=field, mute=True, **filter_kwargs)
    n_non_validated = len(inspect_result.non_validated)
    if n_non_validated == 0:
        logger.success(f"all {organism} variables are validated!")
        validated = True
    else:
        are = "are" if n_non_validated > 1 else "is"
        print_values = _print_values(inspect_result.non_validated)
        logger.warning(
            f"{colors.yellow(f'{n_non_validated} variables')} {are} not validated: "
            f"{colors.yellow(print_values)}\n      → register variables via "
            f"{colors.red('`.register_variables()`')}"
        )
        validated = False
    logger.indent = ""

    ln.settings.verbosity = former_verbosity
    return validated
