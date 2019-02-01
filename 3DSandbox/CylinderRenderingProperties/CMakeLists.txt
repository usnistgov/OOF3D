
cmake_minimum_required(VERSION 2.8)
 
PROJECT(CylinderRenderingProperties)
 
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
 
add_executable(CylinderRenderingProperties MACOSX_BUNDLE CylinderRenderingProperties.cxx )
 
target_link_libraries(CylinderRenderingProperties ${VTK_LIBRARIES})
