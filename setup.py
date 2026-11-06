from setuptools import setup, find_packages

setup(
    name="linux-security-audit-framework",
    version="1.0.0",
    author="Nassim Ammar",
    author_email="nassim@example.com",
    description="Framework d'audit de sécurité automatisé pour infrastructures Linux",
    long_description="""
    Linux Security Audit Framework
    =============================
    
    Un outil complet d'audit de sécurité pour systèmes Linux.
    
    Fonctionnalités:
    - 50+ vérifications de sécurité
    - Scan CVE via API NVD
    - Scoring CVSS
    - Rapports HTML et PDF
    - Interface Web
    - Scan distant SSH
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/nassim/linux-security-audit",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=2.3.0',
        'requests>=2.31.0',
        'reportlab>=4.0.0',
        'psutil>=5.9.0',
    ],
    entry_points={
        'console_scripts': [
            'audit-cli=main:main',
            'audit-web=web_dashboard:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security',
        'Topic :: System :: Systems Administration',
    ],
    python_requires='>=3.10',
)
