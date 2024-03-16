from setuptools import setup
from setuptools import find_packages

setup(
    name='streamlit-signin-auth-ui',

    author='GitSamad88',

    author_email='samadtaoufik@gmail.com',

    version='1.0.0',

    description="A streamlit library which provides a Login/Sign-Up UI with an option to reset password, also supports cookies and"
                "store user's data in a Google Sheets file as database.",


    long_description_content_type="text/markdown",

    url='https://github.com/GitSamad88/streamlit-signin-ui',

    install_requires=[
        'streamlit',
        'streamlit_lottie',
        'extra_streamlit_components',
        'streamlit_option_menu',
        'streamlit_cookies_manager',
        'gspread',
        'argon2',
        'setuptools',
        'google-api-python-client',
        'oauth2client',
        'requests',
        'pandas',
    ],

    keywords='streamlit, machine learning, login, sign-up, authentication, cookies',

    packages=find_packages(),


    include_package_data=True,

    python_requires='>=3.10',

    classifiers=[

        # 'Intended Audience :: Developers',
        # 'Intended Audience :: ML Engineers',
        # 'Intended Audience :: Streamlit App Developers',

        'License :: OSI Approved :: MIT License',

        'Natural Language :: English',

        'Operating System :: OS Independent',

        # 'Programming Language :: Python :: 3.10.12',

        # 'Topic :: Streamlit',
        # 'Topic :: Authentication',
        # 'Topic :: Login/Sign-Up'

    ]
)
