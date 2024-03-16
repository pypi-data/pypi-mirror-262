from info.basic.functions import default_param
from info.basic.decorators import FuncTools
from info.basic.typehint import T, Null
from info.toolbox.libs.operations.logger import exception_logger
from info import docfunc as doc
from pandas import DataFrame
from typing import Generator, Any, Optional
import numpy as np
import os


_warn_msg = 'repeats less than 3, use mean instead, for statistic might not be accurate...'
func = __import__('info.basic.functions', fromlist=['_make_column_name'])
dep = __import__('info.basic.medical', fromlist=['_itk_img'])
_itk_img = getattr(dep, '_itk_img')
_make_column_name = getattr(func, '_make_column_name')
_get_values = getattr(func, '_get_values')
_fea_pick = getattr(func, '_fea_pick')


@FuncTools.params_setting(data=T[Null: Generator], extractor_setting=T[{}: dict[str, Any]],
                          err_file=T[None: Optional[str]], image_types=T[None: Optional[dict[str, dict]]],
                          feature_class=T[None: Optional[dict[str, list[str]]]])
@FuncTools.attach_attr(docstring=doc.radiomics_features, info_func=True, entry_tp=Generator, return_tp=DataFrame)
def radiomics_features(**params):
    radi_prompt = __import__('radiomics', fromlist=['setVerbosity']).setVerbosity
    extractor = __import__('radiomics.featureextractor',
                           fromlist=['RadiomicsFeatureExtractor']).RadiomicsFeatureExtractor
    exe = extractor(**params.get('extractor_setting'))
    conf1, conf2 = params.get('image_types'), params.get('feature_class')
    _ = exe.enableImageTypes(**conf1) if conf1 else exe.enableAllImageTypes()
    exe.enableAllFeatures()  # following customized
    radi_prompt(60)
    has_no_column_names, values, col_names, row_name = True, [], [], []
    err_file = default_param(params, 'err_file', os.path.sep.join([os.getcwd(), 'err_case.log']))
    *_, err_file = err_file.split(os.path.sep)
    err_directory, name = os.path.sep.join(_) if len(_) > 0 else '.', None
    try:
        for name, img, msk, sp in params.get('data'):  # (case_name, img_ndarray, roi_ndarray, spacing)
            try:
                fea = exe.execute(_itk_img(img, sp, None, None), _itk_img(msk, sp, None, None))
                if has_no_column_names:
                    col_names = _make_column_name(fea)
                    has_no_column_names = False
                values.append(_get_values(fea))
                row_name.append(name)
            except (Exception, ) as err:
                exception_logger(data=(name, err), directory=err_directory, to_file=err_file)
    except (Exception, ) as err:
        exception_logger(data=(f'last case {name} before interrupt', err), directory=err_directory, to_file=err_file)

    res = DataFrame([])

    if len(col_names) > 0:
        if conf2:
            idx = np.array([_fea_pick(_, conf2) for _ in col_names])
            res = DataFrame(np.array(values)[:, idx], index=row_name, columns=np.array(col_names)[idx])
        else:
            res = DataFrame(np.array(values), index=row_name, columns=col_names)

    # modify the incorrect result (maybe bug?) from pyradiomics
    # TODO: 1. report to git; 2. version BUG: issue 828 https://github.com/AIM-Harvard/pyradiomics/issues/828

    return res


__all__ = ['radiomics_features']


if __name__ == '__main__':
    pass
