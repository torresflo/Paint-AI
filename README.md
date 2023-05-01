![GitHub license](https://img.shields.io/github/license/torresflo/Paint-AI.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
![GitHub contributors](https://img.shields.io/github/contributors/torresflo/Paint-AI.svg)
![GitHub issues](https://img.shields.io/github/issues/torresflo/Paint-AI.svg)

<p align="center">
  <h1 align="center">Paint AI</h3>

  <p align="center">
    A Python application to generate pictures based on your drawing.
    Based on <a href="https://github.com/CompVis/stable-diffusion">Stable Diffusion</a>.
    <br />
    <a href="https://github.com/torresflo/Paint-AI/issues">Report a bug or request a feature</a>
  </p>
</p>

## Table of Contents

* [Getting Started](#getting-started)
  * [Prerequisites and dependencies](#prerequisites-and-dependencies)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)

## Getting Started

### Prerequisites and dependencies

This repository is tested with Python 3.10+ and PyTorch 2.0.0. It works only on Nvidia graphics cards and CUDA should be installed.

You should install Paint AI in a [virtual environment](https://docs.python.org/3/library/venv.html). If you're unfamiliar with Python virtual environments, check out the [user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
First, create a virtual environment with the version of Python you're going to use and activate it.

You can install directly all required packages by using the file `requirements.txt` and doing:
```bash
pip install -r requirements.txt
```

### Installation

Follow the instructions above then clone the repo (`git clone https:://github.com/torresflo/Paint-AI.git`). 

You can now run `main.py`.

## Usage

The image generation and if it is possible or not will depends of your hardware.
This project has been tested on a Nvidia RTX 3070 with 8Gb of VRAM. With this hardware, it allows to generate images in around 3 seconds with 20 iteration steps.

Enter your prompt and start drawing in the right canvas to generate an image, it is as simple as that!
You can then click on the generated image in the left canvas to save it if you want to.
All generated images have a size of 512x512 pixels.

Here is a small video demonstrating how it works:

https://user-images.githubusercontent.com/50424335/235513123-df814213-ffc1-45da-be12-2cd4e87f596e.mp4

### Available parameters ###

Some parameters are available to tweak the generation:

**Iteration steps:**

You can change the number of iteration steps used to generate the image. In general, results are better the more steps you use. Stable Diffusion, being one of the latest models, works great with a relatively small number of steps (default is 20 so it allows live geneation while drawing). If you want faster results you can use a smaller number, if you want better results, you can use a bigger number.

**Strength:**

Strength is a value between 0.0 and 1.0 that controls the amount of noise added to your drawing. Values that approach 1.0 allow for lots of variations but will also produce images that are not semantically consistent with your drawing.

**Guidance scale:**

The guidance scale is a way to increase the adherence to your prompt as well as overall sample quality. In simple terms, it forces the generation to better match with your prompt. Numbers like 7 or 8.5 give good results, if you use a very large number the images might look good, but will be less diverse.

**Seed:**

If you want deterministic output you can set a random seed that will be given to the image generator. Every time you use the same seed, the same prompt and the same drawing, you will get the same generated image.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.
