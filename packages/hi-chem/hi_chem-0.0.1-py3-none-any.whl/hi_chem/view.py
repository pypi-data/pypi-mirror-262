import py3Dmol
from rdkit import Chem


def view(mol: Chem.Mol, height: int=600, width: int = 600) -> py3Dmol.view:
    """
    A method designed to create a 3D figure with py3Dmol
    """
    mb = Chem.MolToMolBlock(mol)
    p = py3Dmol.view(width=width, height=height)
    p.addModel(mb, "sdf")
    p.setStyle({'stick': {}})
    p.setBackgroundColor('0xeeeeee')
    p.zoomTo()
    return p.show()
