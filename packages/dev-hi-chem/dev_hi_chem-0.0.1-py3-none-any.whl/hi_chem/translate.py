from typing import Union
from rdkit import Chem


def mol_from_smiles(smiles: str, errors_ok: bool = True) -> Union[Chem.Mol, None]:
    try:
        mol = Chem.MolFromSmiles(smiles)
        return mol
    except BaseException as e:
        if errors_ok:
            return None
        raise e


def mol_from_smarts(smarts: str, errors_ok: bool = True) -> Union[Chem.Mol, None]:
    try:
        mol = Chem.MolFromSmarts(smarts)
        return mol
    except BaseException as e:
        if errors_ok:
            return None
        raise e
