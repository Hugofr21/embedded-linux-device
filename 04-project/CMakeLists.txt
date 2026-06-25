cmake_minimum_required(VERSION 3.20)

project(EmbeddedDemo)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Biblioteca
add_library(calculator
    src/calculator.cpp
)

target_include_directories(calculator PUBLIC include)

# Executável
add_executable(app
    src/main.cpp
)

target_link_libraries(app PRIVATE calculator)

# Coverage (aplicado corretamente)
target_compile_options(calculator PRIVATE --coverage)
target_link_options(calculator PRIVATE --coverage)

target_compile_options(app PRIVATE --coverage)
target_link_options(app PRIVATE --coverage)

find_program(CLANG_TIDY_EXE NAMES clang-tidy)

if(CLANG_TIDY_EXE)
    message(STATUS "clang-tidy found: ${CLANG_TIDY_EXE}")

    set(CMAKE_CXX_CLANG_TIDY
        ${CLANG_TIDY_EXE};
        -checks=clang-analyzer-*,modernize-*,performance-*,readability-*
    )
endif()