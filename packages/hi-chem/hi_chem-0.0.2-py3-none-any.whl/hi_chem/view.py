import py3Dmol
from rdkit import Chem
from typing import Union


def view_3d(
    mol: Chem.Mol,
    conf_ids: Union[int, list[int], None] = None,
    height: int = 600,
    width: int = 600
) -> py3Dmol.view:
    """
    A method designed to create a 3D figure with py3Dmol
    """
    if conf_ids is None:
        conf_ids = [conf.GetId() for conf in mol.GetConformers()]
    elif isinstance(conf_ids, int):
        conf_ids = [conf_ids]

    p = py3Dmol.view(width=width, height=height)
    for conf_id in conf_ids:
        mb = Chem.MolToMolBlock(mol, confId=conf_id)
        p.addModel(mb, "sdf")

    p.setStyle({'stick': {}})
    p.setBackgroundColor('0xeeeeee')
    p.zoomTo()
    return p.show()

