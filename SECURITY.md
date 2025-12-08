# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in GPU-SIM:

1. **Do NOT** open a public issue
2. Email the maintainers directly (or use GitHub's private vulnerability reporting)
3. Include detailed information about the vulnerability
4. Wait for confirmation before disclosing publicly

## Security Considerations

GPU-SIM modifies Windows registry entries. This is inherently sensitive:

- Always run in a **virtual machine** for testing
- Create **system restore points** before applying changes
- Run only from **trusted sources**
- Never share registry backups containing sensitive data

## Disclaimer

This software modifies system registry. Use at your own risk.
The authors are not responsible for any damage caused by misuse.
