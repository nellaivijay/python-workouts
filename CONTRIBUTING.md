# Contributing to Python Workouts 🤝

Thank you for your interest in contributing to this repository! This document provides guidelines for contributing to the Python Workouts project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 How to Contribute

### Reporting Bugs

1. Search existing issues to avoid duplicates
2. Create a new issue with a descriptive title
3. Provide detailed information:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details

### Suggesting Enhancements

1. Check if the enhancement is already requested
2. Create a feature request with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Potential implementation approach

### Adding New Scripts

1. Choose an appropriate directory (or create a new one)
2. Follow the existing code structure and style
3. Include comprehensive documentation
4. Add examples and usage instructions
5. Update the README if adding a new category

## 🔧 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account

### Setting Up the Repository

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

```bash
# Run all tests
pytest testing/unit_tests.py -v

# Run specific test file
pytest advanced_testing/pytest_mock_integration.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## 📝 Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Maximum line length: 127 characters

### Code Organization

- One script per file
- Include `if __name__ == "__main__":` block
- Use type hints where appropriate
- Group related functionality together

### Documentation

- Add docstrings to all functions and classes
- Include usage examples in docstrings
- Add comments for complex logic
- Update README for new features

### Testing

- Write tests for new functionality
- Aim for >80% code coverage
- Include both unit and integration tests
- Test edge cases and error conditions

## 🔄 Pull Request Process

### Before Submitting

- [ ] Ensure all tests pass
- [ ] Add/update documentation
- [ ] Follow coding standards
- [ ] Update README if needed
- [ ] Add your name to contributors list

### Submitting PR

1. Push your branch to your fork
2. Create a pull request with:
   - Clear title describing the change
   - Detailed description of changes
   - Reference related issues
   - Screenshots if applicable
3. Wait for review and address feedback

### PR Review Process

- Maintainers will review your PR
- Address any requested changes
- Ensure CI checks pass
- Keep discussions focused and constructive

## 📧 Issue Reporting

### Bug Reports

- Use the bug report template
- Provide reproduction steps
- Include environment details
- Add relevant logs or error messages

### Feature Requests

- Describe the feature clearly
- Explain the use case
- Suggest potential implementation
- Consider impact on existing functionality

## 🎯 Development Priorities

### High Priority
- Bug fixes
- Security vulnerabilities
- Breaking changes

### Medium Priority
- New exercise scripts
- Documentation improvements
- Test coverage

### Low Priority
- Nice-to-have features
- Refactoring
- Style improvements

## 📜 Project Structure

```
python-workouts/
├── basics/              # Basic Python operations
├── data_structures/     # Data structure implementations
├── algorithms/          # Algorithm implementations
├── database_operations/ # Database examples
├── web_development/     # Web framework examples
├── machine_learning/    # ML examples
├── data_visualization/ # Data visualization
├── concurrency/        # Concurrency examples
├── devops_tools/        # DevOps automation
├── security/           # Security examples
├── performance/        # Performance optimization
├── advanced_testing/    # Advanced testing patterns
└── .github/workflows/   # GitHub Actions workflows
```

## 🏆 Recognition

Contributors will be acknowledged in the repository:
- Contributors section in README
- GitHub Contributors list
- Release notes for significant contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.

## 💬 Questions?

Feel free to open an issue for questions about contributing or the project in general.

---

Happy contributing! 🚀