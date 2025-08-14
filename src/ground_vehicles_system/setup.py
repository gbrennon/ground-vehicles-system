from setuptools import find_packages, setup

package_name = "ground_vehicles_system"
package_description = (
    "Ground Vehicles System RO2 package applying Clean Architecture principles"
)

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(where="src", exclude=["test"]),
    package_dir={"": "src"},
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools", "rclpy"],
    zip_safe=True,
    maintainer="Glauber Brennon",
    maintainer_email="glauberbrennon@gmail.com",
    description=package_description,
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            # TODO list entry points here
        ],
    },
)
