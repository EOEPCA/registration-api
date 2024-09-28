<!--
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** rm-workspace-api, __fschindler__, fabian.schindler@eox.at
-->

<!-- PROJECT SHIELDS -->
<!--
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/EOEPCA/registration-api">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">EOEPCA+ Registration API</h3>

  <p align="center">
    This repository includes the EOEPCA+ Registration API component
    <br />
    <a href="https://eoepca.readthedocs.io/projects/resource-registration/en/latest/"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://demo.pygeoapi.io/">View Demo</a>
    ·
    <a href="https://github.com/EOEPCA/registration-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/EOEPCA/registration-api/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Description](#description)
  - [Built With](#built-with)
  - [Interfaces](#interfaces)
- [Getting Started](#getting-started)
  - [Deployment](#deployment)
- [Documentation](#documentation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## Description

The EOEPCA+ Registration API building block is built upon the upstream pygeoapi project.

pygeoapi is a Python server implementation of the OGC API suite of standards.

The project emerged as part of the next generation OGC API efforts in 2018 and provides the capability for organizations to deploy a RESTful OGC API endpoint using OpenAPI, GeoJSON, and HTML.

pygeoapi is open source and released under an MIT license, and runs on all major platforms (Windows, Linux, Mac OS X). It is an official [OSGeo Project](https://www.osgeo.org/projects/pygeoapi/).

pygeoapi is [Certified OGC Compliant](https://www.ogc.org/resources/product-details/?pid=1663) and is an OGC Reference Implementation for [OGC API - Features 1.0](https://www.ogc.org/resource/products/details/?pid=1663), [OGC API - EDR 1.0.1](https://www.ogc.org/resource/products/details/?pid=1663), [OGC API - Tiles 1.0](https://www.ogc.org/resource/products/details/?pid=1663) and [OGC API - Processes 1.0](https://www.ogc.org/resource/products/details/?pid=1826).

### Built With

- [Python](https://www.python.org)
- [pygeoapi](https://pygeoapi.io)

### Interfaces

The Registration API provides the following interfaces:
* OGC API - Processes - Part 1: Core

Internally, Data and Metadata registration can be done by the following ways:
* Transaction interfaces (OGC CSW-T or OGC API - Features - Part 4: Create, Replace, Update, Delete) to EOEPCA Resource Catalogue
* Transaction interfaces (STAC API - Create, Replace, Update, Delete) to EOEPCA Data Catalogue
* Transaction interfaces (OGC API - Features - Part 4: Create, Replace, Update, Delete) to EOEPCA Data Access
* Invoking the EOEPCA Harvester component

pygeoapi implements the following interfaces:
* OGC API - Features 1.0
* OGC API - Environmental Data Retrieval 1.0.1
* OGC API - Tiles 1.0
* OGC API - Coverages 1.0
* OGC API - Maps 1.0
* OGC API - Processes 1.0
* OGC API - Records 1.0
* SpatioTemporal Asset Catalog (STAC) 1.0


<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running in 5 minutes follow these simple steps.

    # Python 3.10 required
    python3 -m venv pygeoapi
    cd pygeoapi
    . bin/activate
    git clone https://github.com/geopython/pygeoapi.git
    cd pygeoapi
    pip3 install -r requirements.txt
    python3 setup.py install
    cp pygeoapi-config.yml example-config.yml
    vim example-config.yml  # edit as required
    export PYGEOAPI_CONFIG=example-config.yml
    export PYGEOAPI_OPENAPI=example-openapi.yml
    pygeoapi openapi generate $PYGEOAPI_CONFIG --output-file $PYGEOAPI_OPENAPI
    pygeoapi serve
    # in another terminal
    curl http://localhost:5000  # or open in a web browser

### Deployment

Registration API deployment is described in the [EOEPCA Deployment Guide](https://deployment-guide.docs.eoepca.org/current/eoepca/registration-api/).

## Documentation

The component documentation can be found at https://docs.pygeoapi.io/en/latest/.

<!-- USAGE EXAMPLES -->

## Usage

Registration API usage documentation is provided through the upstream pygeoapi project.

* [pygeoapi Home Page](https://pygeoapi.io/)
* [pygeoapi Documenation](https://docs.pygeoapi.io/en/latest/)
* [pygeoapi demo](https://demo.pygeoapi.io/)
* [EOEPCA Registration API usage](https://eoepca.readthedocs.io/projects/resource-registration/en/latest/design/registration-api/api/usage/)


<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/geopython/pygeoapi/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

The EOEPCA components are distributed under the Apache-2.0 License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Angelos Tzotsos - [@tzotsos](https://twitter.com/tzotsos) - https://www.osgeo.org/member/angelos-tzotsos/

Project Link: [https://github.com/EOEPCA/registration-api](https://github.com/EOEPCA/registration-api)

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- README.md is based on [this template](https://github.com/othneildrew/Best-README-Template) by [Othneil Drew](https://github.com/othneildrew).

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/EOEPCA/registration-api.svg?style=flat-square
[contributors-url]: https://github.com/EOEPCA/registration-api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/EOEPCA/registration-api.svg?style=flat-square
[forks-url]: https://github.com/EOEPCA/registration-api/network/members
[stars-shield]: https://img.shields.io/github/stars/EOEPCA/registration-api.svg?style=flat-square
[stars-url]: https://github.com/EOEPCA/registration-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/EOEPCA/registration-api.svg?style=flat-square
[issues-url]: https://github.com/EOEPCA/registration-api/issues
[license-shield]: https://img.shields.io/github/license/EOEPCA/registration-api.svg?style=flat-square
[license-url]: https://github.com/EOEPCA/registration-api/blob/master/LICENSE
