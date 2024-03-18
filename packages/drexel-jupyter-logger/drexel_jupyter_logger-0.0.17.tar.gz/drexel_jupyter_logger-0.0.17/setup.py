import setuptools

setuptools.setup(
    name = "drexel_jupyter_logger",
    version= "0.0.17",
    author = "Joshua C. Agar",
    description= "drexel jupyter logger package",
    packages=["drexel_jupyter_logger"],
    install_requires=["cryptography"],
    entry_points={
        'console_scripts': [
            'student-info-from-nb=drexel_jupyter_logger.student_info_from_nb:main',
            'grade-report=drexel_jupyter_logger.grade_report:main',
            'build-quiz-for-jupyterbook=drexel_jupyter_logger.build_quiz_for_jupyterbook:main',
            'read-log-file=drexel_jupyter_logger.read_log_file:main',
            'remove-skip=drexel_jupyter_logger.remove_skip:main',
            'tag-ftiviles=drexel_jupyter_logger.tag_files:main',
            'activity=drexel_jupyter_logger.activity:main',
            'fix_kernel=drexel_jupyter_logger.fix_kernel:main',
            'section_toc=drexel_jupyter_logger.section_toc:main',
            'week_toc=drexel_jupyter_logger.week_toc:main',
            'final_tag=drexel_jupyter_logger.final_tag:main',
        ],
    }
)