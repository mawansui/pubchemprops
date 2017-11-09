************
PubChemProps
************

*Extract experimental properties of any PubChem compound with ease.*

**Documentation:**

1. Why?
2. Installation
3. Usage
4. TODOs

Why?
----

Why, indeed, do we need another PubChem-related python package? The answer is that I've found the `available one`__ not quite fitting my needs. While the mentioned package offers a wide range of possible uses and allows to retrieve various **computed** parameters, it does not allow to retrieve any **experimental** ones. So I decided to write my own package that would do exactly that!

__ https://pypi.python.org/pypi/PubChemPy/1.0.4

Installation
------------

``pip install pubchemprops``

Usage
-----
``from pubchemprops.pubchemprops import X`` ,

where X is one of the following functions:

- ``get_cid_by_name`` – takes a compound name, searches PubChem for it and returns it's PubChem ID
- ``get_first_layer_props`` – takes a compound name and a list of required parameters that CAN be retreived directly using the amazing PubChem PUG REST API
- ``get_second_layer_props`` - takes a compound name and a list of required parameters that CAN NOT be retreived directly and for which one would have to look for in the depth of the whole PubChem record for the compound

What's with the layers?
-----------------------

Just couldn't find any better name for that :] PRs much welcomed if you have another suggestion, though.

Basically what it means is that **first layer** properties are **easy** to retrieve, because there is a clear API for that. Here is the list of these properties: 

``MolecularFormula, MolecularWeight, CanonicalSMILES, IsomericSMILES, InChI, InChIKey, IUPACName, XLogP, ExactMass, MonoisotopicMass, TPSA, Complexity, Charge, HBondDonorCount, HBondAcceptorCount, RotatableBondCount, HeavyAtomCount, IsotopeAtomCount, AtomStereoCount, DefinedAtomStereoCount, UndefinedAtomStereoCount, BondStereoCount, DefinedBondStereoCount, UndefinedBondStereoCount, CovalentUnitCount, Volume3D, XStericQuadrupole3D, YStericQuadrupole3D, ZStericQuadrupole3D, FeatureCount3D, FeatureAcceptorCount3D, FeatureDonorCount3D, FeatureAnionCount3D, FeatureCationCount3D, FeatureRingCount3D, FeatureHydrophobeCount3D, ConformerModelRMSD3D, EffectiveRotorCount3D, ConformerCount3D, Fingerprint2D``

Whoa, that's hell of a lot of properties, and you can ask for any of those with the ``get_first_layer_props`` function. Use it like that:

``easy_properties = get_first_layer_props('acetone', ['MolecularWeight', 'IUPACName', 'CanonicalSMILES', 'InChI'])``

``print(easy_properties)`` will return

``{'CID': 180, 'MolecularWeight': 58.08, 'CanonicalSMILES': 'CC(=O)C', 'InChI': 'InChI=1S/C3H6O/c1-3(2)4/h1-2H3', 'IUPACName': 'propan-2-one'}``
