# UE5 Car Rigging Addon for Blender

A Blender addon for rigging vehicles for Unreal Engine 5, with improved bone placement and hierarchy structure.

## Features

- Automatic vehicle rigging for UE5
- Clean bone hierarchy with root-based structure
- Precise bone placement matching mesh transforms
- Support for wheels, brake calipers, and dashboard instruments
- Dynamic wheel count support

## Installation

1. Download the latest release ZIP file
2. In Blender, go to Edit → Preferences → Add-ons
3. Click "Install..." and select the ZIP file
4. Enable the "UE4 Vehicle Rigging Addon" in the add-ons list

## Usage

1. Select your vehicle base mesh and wheel meshes
2. Optionally select brake calipers and dashboard instruments
3. Use the Vehicle Rigging panel in the 3D viewport
4. Click "Rig Vehicle" to generate the armature

## Improvements in This Version

- ✅ Brake caliper bones are now children of the root bone (not wheel bones)
- ✅ All bones are precisely placed at mesh origins with correct rotation
- ✅ Improved bone hierarchy for better UE5 compatibility

## License

This project is licensed under the GNU General Public License v3.0 - see the GPL3-license.txt file for details.

## Credits

Based on the original UE4 Vehicle Rigging Addon by Arturs Ontuzans
Extended and improved for better UE5 compatibility.
