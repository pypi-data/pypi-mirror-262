# Security Header Scan (shscan)

<p align="center">
    <img src="google.png" alt="Result of the google" />
</p>

## SHScan description:

The "SHScan" tool was developed with the purpose of assisting in checking the security headers enabled on specific or internal websites. Created to simplify this process, the tool is notable for its simplicity and efficiency, representing the result in an intuitive way.

Its operation is straightforward: by providing a URL as input, the tool checks the security headers associated with the website and generates a detailed report indicating which are enabled or not.

Although its initial implementation is basic, the tool demonstrates great potential for improvement and expansion. The code is open for contributions and suggestions for improvement, and the developer is receptive to any form of collaboration to make the tool more robust and useful for the community.

## How to run:

### Pypi
```bash
pip install shscan
shscan https://example.com.br
```

### From source
```bash
git clone https://github.com/boyinf/shscan && cd shscan
python ./shscan.py https://example.com.br
```

## Usage
```
Usage: shscan <target>

Options:
  -ssl            Test the URL with SSL enabled.
```