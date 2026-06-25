#!/bin/bash

set -e

echo "Cleaning..."
rm -rf build metrics code_cov

mkdir -p build
mkdir -p metrics
mkdir -p code_cov

START_TIME=$(date +%s)

echo "Configuring..."
cmake -S . -B build -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

echo "Clang-Tidy..."
clang-tidy -p build src/*.cpp || true

echo "Building..."
cmake --build build

echo "Running app..."
./build/app

END_TIME=$(date +%s)

BUILD_TIME=$((END_TIME - START_TIME))

echo "Generating coverage..."
gcovr -r . --html --html-details -o code_cov/coverage.html

echo "Writing KPIs..."

cat > metrics/kpis.json <<EOF
{
  "build_time_seconds": ${BUILD_TIME},
  "build_status": "success"
}
EOF

echo "KPIs written successfully:"
cat metrics/kpis.json