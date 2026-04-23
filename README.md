# batch_import_images_to_brushes
Batch import images as texture paint and sculpt brushes with automatic preview generation

# Batch Import Images to Brushes

[![Blender Version](https://img.shields.io/badge/Blender-5.1%2B-blue)](https://www.blender.org/)
[![License](https://img.shields.io/badge/License-GPL--3.0--or--later-green)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Extensions](https://img.shields.io/badge/Blender-Extensions-orange)](https://extensions.blender.org/)

**Batch import images as texture paint and sculpt brushes with automatic preview generation**

## Overview

Batch Import Images to Brushes streamlines the process of converting multiple images into fully functional Blender brushes. Simply select your image files, and the addon automatically creates textures, brushes, and preview thumbnails for both Texture Paint and Sculpt modes.

Perfect for artists who need to import large collections of alpha textures, skin details, or custom brush stamps.

## Features

### Batch Import

- **Multi-file selection** - Import hundreds of images at once
- **Smart naming** - Preserve original filenames or add custom prefixes/suffixes
- **Duplicate detection** - Automatically skips existing brushes

### Supported Formats

- PNG, JPEG, JPEG2000
- BMP, TIFF, TARGA
- WEBP, HDR

### Dual Brush Creation

- **Texture Paint Brushes** - Create image-based painting brushes
- **Sculpt Brushes** - Convert images to sculpting alphas
- **Both Modes** - Generate both brush types simultaneously

### Automatic Preview Generation

- **Smart thumbnails** - Creates 256x256 previews from source images
- **Asset library ready** - Automatically marks brushes as assets
- **Custom icons** - Each brush gets a unique visual identifier

### Brush Settings

- **Adjustable properties** - Set size, strength, and tool type per mode
- **Texture controls** - Configure alpha calculation, inversion, and interpolation
- **Flexible naming** - Add prefixes/suffixes for better organization

## Installation

### As a Blender Extension (Recommended)

1. Download the latest `.zip` file from [Releases](../../releases)
2. In Blender, go to `Edit` > `Preferences` > `Extensions`
3. Click the dropdown menu (⋮) and select `Install from Disk`
4. Navigate to and select the downloaded `.zip` file
5. Enable the addon in the Extensions list

### As a Legacy Addon

1. Download the latest `.zip` file from [Releases](../../releases)
2. Extract the contents to your Blender addons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\5.1\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/5.1/scripts/addons/`
   - **Linux**: `~/.config/blender/5.1/scripts/addons/`
3. Rename the folder to `batch_import_images_to_brushes`
4. In Blender, go to `Edit` > `Preferences` > `Add-ons`
5. Search for "Batch Import Images to Brushes"
6. Enable the addon

## Usage

### Basic Workflow

1. **Prepare your images**
   - Collect your brush textures in a folder
   - PNG files with transparency work best for alpha brushes

2. **Import**
   - Go to `File` > `Import` > `Images as Brushes`
   - Select your image files
   - Choose brush type (Texture Paint, Sculpt, or Both)

3. **Configure**
   - Adjust size and strength for each brush mode
   - Set naming options (prefix/suffix)
   - Toggle preview generation

4. **Start painting**
   - Find your new brushes in the brush selector
   - Previews are visible in the asset browser
   - Brushes are ready to use immediately

### Settings Reference

| Setting | Description |
|---------|-------------|
| **Brush Type** | Texture Paint, Sculpt, or Both |
| **Strength** | Brush intensity (0.0 to 2.0) |
| **Size** | Brush radius in pixels (1 to 500) |
| **Sculpt Tool** | Draw, Clay, Smooth, Crease, Flatten, Fill |
| **Name Prefix/Suffix** | Add custom text to brush names |
| **Generate Preview** | Create thumbnails from source images |

## Use Cases

### Texture Artists

- Import skin pore details
- Add wrinkle and crease stamps
- Build custom brush libraries

### Sculptors

- Convert alphas to sculpt brushes
- Import displacement maps
- Create detail stamp collections

### Character Artists

- Batch import skin texture brushes
- Add facial detail stamps (lips, pores, wrinkles)
- Build reusable brush kits

### Environment Artists

- Import foliage and vegetation alphas
- Add surface detail brushes
- Create texture variation stamps

## Tips and Best Practices

### For Best Results

- Use square images for even brush scaling
- PNG format preserves alpha transparency
- Higher resolution images create better previews

### Organization

- Enable "Use name prefix/suffix" to add categories
- Example: `skin_` prefix + `_alpha` suffix = `skin_porcelain_alpha`

### Performance

- The addon packs images into your .blend file
- No external file dependencies after import
- Previews are cached for quick loading

## File Structure

batch_import_images_to_brushes/
├── init.py # Main addon code
├── blender_manifest.toml # Extension manifest
└── README.md # This file


## Requirements

- **Blender**: Version 5.1.0 or higher
- **Platform**: Windows, macOS, Linux
- **Python**: Built-in Blender Python (no external dependencies)

## Known Limitations

- Very large images (>4096x4096) may cause slow preview generation
- Non-square images are automatically centered in a square canvas
- Brush thumbnails are scaled to 256x256 pixels

## Troubleshooting

### Brushes don't appear in the brush selector

- Try toggling between paint/sculpt modes
- Check that the brush type matches your current mode
- Restart Blender if necessary

### Previews aren't generating

- Ensure "Generate Preview" is enabled in settings
- Check that images are properly loaded (not missing)
- Try re-importing the images

### Import fails for some files

- Verify the file format is supported (PNG, JPEG, etc.)
- Check that the file isn't corrupted
- Ensure the file path doesn't contain special characters

## Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue with detailed reproduction steps
2. **Suggest features** - Submit feature requests through issues
3. **Submit code** - Fork the repository and create a pull request

### Development Setup

1. Clone the repository
2. Symlink or copy the folder to your Blender addons directory
3. Enable the addon in Blender
4. Make changes and test in Blender

## License

This project is licensed under the **GPL-3.0-or-later** license.

See the [LICENSE](LICENSE) file for details.

## Links

- [Blender Extensions Platform](https://extensions.blender.org/)
- [Report an Issue](../../issues)
- [Blender Documentation](https://docs.blender.org/)

## Changelog

### Version 1.0.0

- Initial release
- Support for multiple image formats
- Texture paint and sculpt brush creation
- Automatic preview generation
- Blender 5.1+ extension system support

## Credits

- **Author**: Raja Muda
---
