# Contributing to GPU-SIM

Thank you for your interest in contributing to GPU-SIM! 🎮

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System info (Windows version, Python version)

### Feature Requests

Open an issue with the `enhancement` label describing:
- The feature you'd like
- Why it would be useful
- Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Commit: `git commit -m "Add amazing feature"`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup

```bash
# Clone
git clone https://github.com/SplashCodeDex/GPU-SIM.git
cd GPU-SIM

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run the app
python src/main.py
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to functions and classes
- Keep functions focused and small

## Project Structure

```
GPU-SIM/
├── src/           # Main application code
├── nvidia_panel/  # NVIDIA Control Panel replica
├── config/        # GPU profiles
├── tests/         # Unit tests
├── docs/          # Documentation
└── build/         # Build scripts
```

## Testing

- Write tests for new features
- Ensure existing tests pass
- Test on Windows (primary platform)

## License

By contributing, you agree your code will be licensed under MIT.
