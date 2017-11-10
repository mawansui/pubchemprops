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

Whoa, ain't that a hell of a lot of properties? And you can ask for any of those with the ``get_first_layer_props`` function! Use it like that:

``easy_properties = get_first_layer_props('acetone', ['MolecularWeight', 'IUPACName', 'CanonicalSMILES', 'InChI'])``

``print(easy_properties)`` will return

``{'CID': 180, 'MolecularWeight': 58.08, 'CanonicalSMILES': 'CC(=O)C', 'InChI': 'InChI=1S/C3H6O/c1-3(2)4/h1-2H3', 'IUPACName': 'propan-2-one'}``

Okay, now moving on to the **second layer**. The name presumes that these properties are much harder to retrieve and you have to dig deeper to get to them. There is no direct API to acceess them or present them in a nice way. Still there are some pretty much interesting properties that you can get out of that:

``IUPAC Name, InChI, InChI Key, Canonical SMILES, Wikipedia, Boiling Point, Melting Point, Flash Point, Solubility, Density, Vapor Density, Vapor Pressure, LogP, Stability, Auto-Ignition, Viscosity, Heat of Combustion, Heat of Vaporization, Surface Tension, Ionization Potential, Dissociation Constants``

Also pretty big list, right? And you can get retrieve any property you like using the ``get_second_layer_props`` (provided there is a record for that property on PubChem itself). Example would be like following:

``lysine_props = get_second_layer_props('L-lysine', ['IUPAC Name', 'Canonical SMILES', 'Boiling Point', 'Vapor Pressure', 'LogP'])``

``print(lysine_props)`` will return a dictionary like this:

``{'IUPAC Name': [{'ReferenceNumber': 38, 'Name': 'IUPAC Name', 'StringValue': '(2S)-2,6-diaminohexanoic acid'}], 'Canonical SMILES': [{'ReferenceNumber': 38, 'Name': 'Canonical SMILES', 'StringValue': 'C(CCN)CC(C(=O)O)N'}], 'Vapor Pressure': [{'ReferenceNumber': 22, 'Name': 'Vapor Pressure', 'Description': '**PEER REVIEWED**', 'Reference': ['Daubert, T.E., R.P. Danner. Physical and Thermodynamic Properties of Pure Chemicals Data Compilation. Washington, D.C.: Taylor and Francis, 1989.'], 'StringValue': '5.28X10+9 mm Hg at 25 deg C /extrapolated/'}], 'LogP': [{'ReferenceNumber': 13, 'Name': 'LogP', 'Reference': ['HANSCH,C ET AL. (1995)'], 'NumValue': -3.05}, {'ReferenceNumber': 22, 'Name': 'LogP', 'Description': '**PEER REVIEWED**', 'Reference': ['Hansch, C., Leo, A., D. Hoekman. Exploring QSAR - Hydrophobic, Electronic, and Steric Constants. Washington, DC: American Chemical Society., 1995., p. 25'], 'StringValue': 'log Kow = -3.05'}, {'ReferenceNumber': 24, 'Name': 'LogP', 'Reference': ['HANSCH,C ET AL. (1995)'], 'StringValue': '-3.05'}]}``

Looking messier than the first layer props return, but I didn't call 'em the second layer props for no reason, you see. :)

Still this is much better than having no info at all!

TODOs
-----

There is still a lot of work to be done:

1. Add error handlers – oftentimes users will not provide a correct compound name due to typos or whatever, so we'd need to add some handlers for that. Ain't got none at the moment.
2. Add more functionality – there are still lots of things one can retrieve from PubChem: images, spectra, bioinformation... 
3. Write better docs maybe
4. Make the data returned look better and easier to read
5. ???
6. PROFIT!

PRs are very much welcomed, also feel free to open any issues or start discussions. 

Hope you like the package!
