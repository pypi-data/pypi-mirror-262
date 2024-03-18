# %%
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem


# %%
def generate_conformers(
        mol: Chem.Mol,
        n_conf: int = 1,
        delta: float = 10,
        n_threads: int = 0,
        remove_high_e_confs: bool = True,
        align: bool = True,
) -> tuple[Chem.Mol, pd.DataFrame, pd.Series]:
    """
    mol: rdkit.Chem.Mol
    n_conf: int
    delta: float, only accept conformers if they are within delta_e of the lowest energy conformer
    n_threads: int, number of threads to run with. 0 defaults to all available threads
    remove_high_e_confs: bool, if True, remove high energy conformers from the `mol`
    align: bool, if True, align the conformers by minimizing the RMSD

    returns:
    mol: rdkit.Chem.Mol, updated molecule with conformers
    energies: pd.DataFrame, conformer indexes, energies, and convergence
    mask: pd.Series, a mask of booleans for each conformer evaluated if they passed validation
    """
    mol = Chem.AddHs(mol)
    ids = AllChem.EmbedMultipleConfs(
        mol,
        numConfs=n_conf,
        useBasicKnowledge=True, # - useBasicKnowledge : impose basic knowledge such as flat rings
        enforceChirality=True,
        numThreads=n_threads,
        randomSeed=42,
    )

    results = AllChem.UFFOptimizeMoleculeConfs(mol, numThreads=n_threads)
    energies = []
    for _id, result in zip(ids, results):
        not_converged, energy = result
        energies.append(
            {
                "id": _id,
                "not_converged": not_converged,
                "energy": energy
            }
        )
    energies = pd.DataFrame(energies)

    # unsure about the units of energy
    low_energy_mask = energies["energy"] <= energies["energy"].min() + delta
    #  if not_converged == 0, then the geometry didn't converge.
    #converged_mask = energies["not_converged"] != 0
    mask = low_energy_mask #& converged_mask

    if remove_high_e_confs:
        for _id in energies[~mask]["id"]:
            mol.RemoveConformer(_id)
            # unsure if this will alter the ids of the remaining conformers?

    if align:
        # align the conformers, for visualization.
        AllChem.AlignMolConformers(mol)

    return mol, energies, mask


#%%

