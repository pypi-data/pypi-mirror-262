#include <mapbox/geojson.hpp>

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "geobuf/geojson_cropping.hpp"
#include "geobuf/geojson_helpers.hpp"
#include "geobuf/pybind11_helpers.hpp"
#include "geobuf/rapidjson_helpers.hpp"

// #define PYBIND11_GEOJSON_WITH_GEOBUF
// #if PYBIND11_GEOJSON_WITH_GEOBUF
// #endif
#include "geobuf.hpp"

#include <fstream>
#include <iostream>

// https://pybind11.readthedocs.io/en/stable/advanced/cast/stl.html?highlight=stl#making-opaque-types
PYBIND11_MAKE_OPAQUE(mapbox::geojson::geometry_collection::container_type);
PYBIND11_MAKE_OPAQUE(mapbox::geojson::multi_line_string::container_type);
PYBIND11_MAKE_OPAQUE(mapbox::geojson::multi_point::container_type);
PYBIND11_MAKE_OPAQUE(mapbox::geojson::multi_polygon::container_type);
PYBIND11_MAKE_OPAQUE(mapbox::geojson::polygon::container_type);
PYBIND11_MAKE_OPAQUE(mapbox::geojson::value::array_type);
PYBIND11_MAKE_OPAQUE(mapbox::geojson::value::object_type);
PYBIND11_MAKE_OPAQUE(std::vector<mapbox::geojson::feature>);

namespace cubao
{
namespace py = pybind11;
using namespace pybind11::literals;
using rvp = py::return_value_policy;

using PropertyMap = mapbox::geojson::value::object_type;

template <typename T> Eigen::VectorXd geom2bbox(const T &t, bool with_z)
{
    auto bbox = mapbox::geometry::envelope(t);
    if (with_z) {
        return (Eigen::VectorXd(6) << //
                    bbox.min.x,
                bbox.min.y, bbox.min.z, //
                bbox.max.x, bbox.max.y, bbox.max.z)
            .finished();
    } else {
        return (Eigen::VectorXd(4) << //
                    bbox.min.x,
                bbox.min.y, //
                bbox.max.x, bbox.max.y)
            .finished();
    }
}

inline bool endswith(const std::string &text, const std::string &suffix)
{
    if (text.length() < suffix.length()) {
        return false;
    }
    return 0 == text.compare(text.length() - suffix.length(), suffix.length(),
                             suffix);
}

void bind_geojson(py::module &geojson)
{
#define is_geojson_type(geojson_type)                                          \
    .def("is_" #geojson_type, [](const mapbox::geojson::geojson &self) {       \
        return self.is<mapbox::geojson::geojson_type>();                       \
    })
#define as_geojson_type(geojson_type)                                          \
    .def(                                                                      \
        "as_" #geojson_type,                                                   \
        [](mapbox::geojson::geojson &self)                                     \
            -> mapbox::geojson::geojson_type & {                               \
            return self.get<mapbox::geojson::geojson_type>();                  \
        },                                                                     \
        rvp::reference_internal)

#define GEOMETRY_DEDUPLICATE_XYZ(geom_type)                                    \
    .def("deduplicate_xyz", [](mapbox::geojson::geom_type &self) {             \
        return deduplicate_xyz(self);                                          \
    })

#define copy_deepcopy_clone(Type)                                              \
    .def("__copy__", [](const Type &self, py::dict) -> Type { return self; })  \
        .def(                                                                  \
            "__deepcopy__",                                                    \
            [](const Type &self, py::dict) -> Type { return self; }, "memo"_a) \
        .def("clone", [](const Type &self) -> Type { return self; })

    py::class_<mapbox::geojson::geojson>(geojson, "GeoJSON", py::module_local())
        is_geojson_type(geometry)           //
        is_geojson_type(feature)            //
        is_geojson_type(feature_collection) //
        as_geojson_type(geometry)           //
        as_geojson_type(feature)            //
        as_geojson_type(feature_collection) //
                                            //
            .def(py::self == py::self)      //
            .def(py::self != py::self)      //
            .def(py::init<>())
            .def(py::init([](const mapbox::geojson::geometry &g) { return g; }))
            .def(py::init([](const mapbox::geojson::feature &g) { return g; }))
            .def(py::init([](const mapbox::geojson::feature_collection &g) {
                return g;
            })) //
            .def(
                "round",
                [](mapbox::geojson::geojson &self, int lon, int lat,
                   int alt) -> mapbox::geojson::geojson & {
                    self.match(
                        [&](mapbox::geojson::geometry &g) {
                            round_coords(g, lon, lat, alt);
                        },
                        [&](mapbox::geojson::feature &f) {
                            round_coords(f.geometry, lon, lat, alt);
                        },
                        [&](mapbox::geojson::feature_collection &fc) {
                            for (auto &f : fc) {
                                round_coords(f.geometry, lon, lat, alt);
                            }
                        },
                        [](auto &) {});
                    return self;
                },
                py::kw_only(), "lon"_a = 8, "lat"_a = 8, "alt"_a = 3,
                rvp::reference_internal)  //
        GEOMETRY_DEDUPLICATE_XYZ(geojson) //
            .def(
                "from_rapidjson",
                [](mapbox::geojson::geojson &self,
                   const RapidjsonValue &json) -> mapbox::geojson::geojson & {
                    self = mapbox::geojson::convert(json);
                    return self;
                },
                rvp::reference_internal)
            .def("to_rapidjson",
                 [](const mapbox::geojson::geojson &self) {
                     RapidjsonAllocator allocator;
                     auto json = mapbox::geojson::convert(self, allocator);
                     return json;
                 })
            .def(
                "from_geobuf",
                [](mapbox::geojson::geojson &self,
                   const std::string &bytes) -> mapbox::geojson::geojson & {
                    self = mapbox::geobuf::Decoder().decode(bytes);
                    return self;
                },
                rvp::reference_internal)
            .def(
                "to_geobuf",
                [](const mapbox::geojson::geojson &self, //
                   int precision, bool only_xy, std::optional<int> round_z) {
                    auto bytes = mapbox::geobuf::Encoder(
                                     std::pow(10, precision), only_xy, round_z)
                                     .encode(self);
                    return py::bytes(bytes);
                },
                py::kw_only(),       //
                "precision"_a = 8,   //
                "only_xy"_a = false, //
                "round_z"_a = std::nullopt)
            //
            .def(
                "crop",
                [](mapbox::geojson::geojson &self, const RowVectors &polygon,
                   const std::string &clipping_mode,
                   std::optional<double> max_z_offset)
                    -> mapbox::geojson::feature_collection {
                    return cubao::geojson_cropping(self,          //
                                                   polygon,       //
                                                   clipping_mode, //
                                                   max_z_offset);
                },
                "polygon"_a, py::kw_only(),    //
                "clipping_mode"_a = "longest", //
                "max_z_offset"_a = std::nullopt)
            //
            .def(
                "load",
                [](mapbox::geojson::geojson &self,
                   const std::string &path) -> mapbox::geojson::geojson & {
                    if (endswith(path, ".pbf")) {
                        auto bytes = mapbox::geobuf::load_bytes(path);
                        self = mapbox::geobuf::Decoder().decode(bytes);
                        return self;
                    }
                    auto json = load_json(path);
                    self = mapbox::geojson::convert(json);
                    return self;
                },
                rvp::reference_internal)
            .def(
                "dump",
                [](const mapbox::geojson::geojson &self, //
                   const std::string &path,              //
                   bool indent,                          //
                   bool sort_keys,                       //
                   int precision,                        //
                   bool only_xy) {
                    if (endswith(path, ".pbf")) {
                        auto bytes = mapbox::geobuf::Encoder(
                                         std::pow(10, precision), only_xy)
                                         .encode(self);
                        return mapbox::geobuf::dump_bytes(path, bytes);
                    }
                    RapidjsonAllocator allocator;
                    auto json = mapbox::geojson::convert(self, allocator);
                    sort_keys_inplace(json);
                    return dump_json(path, json, indent);
                },
                "path"_a, py::kw_only(), //
                "indent"_a = false,      //
                "sort_keys"_a = false,   //
                "precision"_a = 8,       //
                "only_xy"_a = false)     //
        copy_deepcopy_clone(mapbox::geojson::geojson)
            .def("__call__",
                 [](const mapbox::geojson::geojson &self) {
                     return self.match(
                         [&](const mapbox::geojson::geometry &g) {
                             return to_python(g);
                         },
                         [&](const mapbox::geojson::feature &f) {
                             return to_python(f);
                         },
                         [&](const mapbox::geojson::feature_collection &fc) {
                             return to_python(fc);
                         },
                         [](const auto &) -> py::object { return py::none(); });
                 })
        //
        ;

#define GEOMETRY_ROUND_COORDS(geom_type)                                       \
    .def(                                                                      \
        "round",                                                               \
        [](mapbox::geojson::geom_type &self, int lon, int lat,                 \
           int alt) -> mapbox::geojson::geom_type & {                          \
            round_coords(self, lon, lat, alt);                                 \
            return self;                                                       \
        },                                                                     \
        py::kw_only(), "lon"_a = 8, "lat"_a = 8, "alt"_a = 3,                  \
        rvp::reference_internal)

    py::bind_vector<mapbox::geojson::multi_point::container_type>(geojson,
                                                                  "coordinates")
        .def(
            "as_numpy",
            [](std::vector<mapbox::geojson::point> &self)
                -> Eigen::Map<RowVectors> {
                return Eigen::Map<RowVectors>(&self[0].x, //
                                              self.size(), 3);
            },
            rvp::reference_internal)
        .def("to_numpy",
             [](const std::vector<mapbox::geojson::point> &self) -> RowVectors {
                 return Eigen::Map<const RowVectors>(&self[0].x, //
                                                     self.size(), 3);
             }) //
        .def(
            "from_numpy",
            [](std::vector<mapbox::geojson::point> &self,
               const Eigen::Ref<const MatrixXdRowMajor> &points)
                -> std::vector<mapbox::geojson::point> & {
                eigen2geom(points, self);
                return self;
            },
            rvp::reference_internal)
        //
        ;

#define is_geometry_type(geom_type)                                            \
    .def("is_" #geom_type, [](const mapbox::geojson::geometry &self) {         \
        return self.is<mapbox::geojson::geom_type>();                          \
    })
#define as_geometry_type(geom_type)                                            \
    .def(                                                                      \
        "as_" #geom_type,                                                      \
        [](mapbox::geojson::geometry &self) -> mapbox::geojson::geom_type & {  \
            return self.get<mapbox::geojson::geom_type>();                     \
        },                                                                     \
        rvp::reference_internal)

    using GeometryBase = mapbox::geometry::geometry_base<double, std::vector>;
    py::class_<GeometryBase>(geojson, "GeometryBase", py::module_local());
    py::class_<mapbox::geojson::geometry, GeometryBase>(geojson, "Geometry",
                                                        py::module_local())
        .def(py::init<>())
        .def(py::init([](const mapbox::geojson::point &g) { return g; }))
        .def(py::init([](const mapbox::geojson::multi_point &g) { return g; }))
        .def(py::init([](const mapbox::geojson::line_string &g) { return g; }))
        .def(py::init(
            [](const mapbox::geojson::multi_line_string &g) { return g; }))
        .def(py::init([](const mapbox::geojson::polygon &g) { return g; }))
        .def(
            py::init([](const mapbox::geojson::multi_polygon &g) { return g; }))
        .def(py::init(
            [](const mapbox::geojson::geometry_collection &g) { return g; }))
        .def(py::init([](const mapbox::geojson::geometry &g) { return g; }))
        .def(py::init(
            [](const mapbox::geojson::geometry_collection &g) { return g; }))
        .def(py::init(
            [](const RapidjsonValue &g) {
                return mapbox::geojson::convert<mapbox::geojson::geometry>(g);
            }))
        .def(py::init(
            [](const py::dict &g) {
                auto json = to_rapidjson(g);
                return mapbox::geojson::convert<mapbox::geojson::geometry>(json);
            }))
        // check geometry type
        is_geometry_type(empty)               //
        is_geometry_type(point)               //
        is_geometry_type(line_string)         //
        is_geometry_type(polygon)             //
        is_geometry_type(multi_point)         //
        is_geometry_type(multi_line_string)   //
        is_geometry_type(multi_polygon)       //
        is_geometry_type(geometry_collection) //
        // convert geometry type
        as_geometry_type(point)               //
        as_geometry_type(line_string)         //
        as_geometry_type(polygon)             //
        as_geometry_type(multi_point)         //
        as_geometry_type(multi_line_string)   //
        as_geometry_type(multi_polygon)       //
        as_geometry_type(geometry_collection) //
        .def(
            "__getitem__",
            [](mapbox::geojson::geometry &self,
               const std::string &key) -> mapbox::geojson::value & {
                return self.custom_properties.at(key);
            },
            "key"_a, rvp::reference_internal) //
        .def(
            "get",
            [](mapbox::geojson::geometry &self,
               const std::string &key) -> mapbox::geojson::value * {
                auto &props = self.custom_properties;
                auto itr = props.find(key);
                if (itr == props.end()) {
                    return nullptr;
                }
                return &itr->second;
            },
            "key"_a, rvp::reference_internal)
        .def("__setitem__",
             [](mapbox::geojson::geometry &self, const std::string &key,
                const py::object &value) {
                 if (key == "type" || key == "coordinates" || key == "geometries") {
                     throw pybind11::key_error(key);
                 }
                 self.custom_properties[key] = to_geojson_value(value);
                 return value;
             })
        .def("__delitem__",
             [](mapbox::geojson::geometry &self, const std::string &key) {
                 return self.custom_properties.erase(key);
             })
        .def("__len__",
             [](mapbox::geojson::geometry &self) { return __len__(self); })
        .def(
            "push_back",
            [](mapbox::geojson::geometry &self,
               const mapbox::geojson::point &point)
                -> mapbox::geojson::geometry & {
                geometry_push_back(self, point);
                return self;
            },
            rvp::reference_internal)
        .def(
            "push_back",
            [](mapbox::geojson::geometry &self,
               const Eigen::VectorXd &point) -> mapbox::geojson::geometry & {
                geometry_push_back(self, point);
                return self;
            },
            rvp::reference_internal)
        .def(
            "push_back",
            [](mapbox::geojson::geometry &self,
               const Eigen::Ref<const MatrixXdRowMajor> &points)
                -> mapbox::geojson::geometry & {
                geometry_push_back(self, points);
                return self;
            },
            rvp::reference_internal)
        .def(
            "push_back",
            [](mapbox::geojson::geometry &self,
               const mapbox::geojson::geometry &geom)
                -> mapbox::geojson::geometry & {
                if (self.is<mapbox::geojson::multi_polygon>() && geom.is<mapbox::geojson::polygon>()) {
                    self.get<mapbox::geojson::multi_polygon>().push_back(geom.get<mapbox::geojson::polygon>());
                } else {
                    geometry_push_back(self, geom);
                }
                return self;
            },
            rvp::reference_internal)
        .def(
            "push_back",
            [](mapbox::geojson::geometry &self,
               const mapbox::geojson::polygon &geom)
                -> mapbox::geojson::geometry & {
                    if (self.is<mapbox::geojson::multi_polygon>()) {
                        self.get<mapbox::geojson::multi_polygon>().push_back(geom);
                    } else {
                        std::cerr << "can only push_back Polygon to MultiPolygon, current type: " << geometry_type(self) << std::endl;
                    }
                return self;
            },
            rvp::reference_internal)
        .def(
            "push_back",
            [](mapbox::geojson::geometry &self,
               const mapbox::geojson::line_string &geom)
                -> mapbox::geojson::geometry & {
                    if (self.is<mapbox::geojson::multi_line_string>()) {
                        self.get<mapbox::geojson::multi_line_string>().push_back(geom);
                    } else {
                        std::cerr << "can only push_back LineString to MultiLineString, current type: " << geometry_type(self) << std::endl;
                    }
                return self;
            },
            rvp::reference_internal)
        .def(
            "pop_back",
            [](mapbox::geojson::geometry &self) -> mapbox::geojson::geometry & {
                geometry_pop_back(self);
                return self;
            },
            rvp::reference_internal)
        .def(
            "resize",
            [](mapbox::geojson::geometry &self, int size) -> mapbox::geojson::geometry & {
                geometry_resize(self, size);
                return self;
            },
            rvp::reference_internal)
        .def(
            "clear",
            [](mapbox::geojson::geometry &self) -> mapbox::geojson::geometry & {
                geometry_clear(self);
                self.custom_properties.clear();
                return self;
            },
            rvp::reference_internal)
        .def("type",
             [](const mapbox::geojson::geometry &self) {
                 return geometry_type(self);
             })
        //
        .def(
            "as_numpy",
            [](mapbox::geojson::geometry &self) -> Eigen::Map<RowVectors> {
                return as_row_vectors(self);
            },
            rvp::reference_internal)
        .def("to_numpy",
             [](const mapbox::geojson::geometry &self) -> RowVectors {
                 return as_row_vectors(self);
             }) //
        .def(
            "from_numpy",
            [](mapbox::geojson::geometry &self,
               const Eigen::Ref<const MatrixXdRowMajor> &points)
                -> mapbox::geojson::geometry & {
                eigen2geom(points, self);
                return self;
            },
            rvp::reference_internal) //
        // dumps, loads, from/to rapidjson
        copy_deepcopy_clone(mapbox::geojson::geometry)
        .def(py::pickle(
            [](const mapbox::geojson::geometry &self) {
                return to_python(self);
            },
            [](py::object o) -> mapbox::geojson::geometry {
                auto json = to_rapidjson(o);
                return mapbox::geojson::convert<mapbox::geojson::geometry>(
                    json);
            }))
        // custom_properties
        BIND_PY_FLUENT_ATTRIBUTE(mapbox::geojson::geometry,  //
                                 PropertyMap,               //
                                 custom_properties)         //
            .def("keys",
                 [](mapbox::geojson::geometry &self) {
                     return py::make_key_iterator(self.custom_properties);
                 }, py::keep_alive<0, 1>())
            .def("values",
                 [](mapbox::geojson::geometry &self) {
                     return py::make_value_iterator(self.custom_properties);
                 }, py::keep_alive<0, 1>())
            .def("items",
                 [](mapbox::geojson::geometry &self) {
                     return py::make_iterator(self.custom_properties);
                 },
                 py::keep_alive<0, 1>())

        .def(
            "__iter__",
            [](mapbox::geojson::geometry &self) {
                return py::make_key_iterator(self.custom_properties);
            },
            py::keep_alive<0, 1>())
        GEOMETRY_ROUND_COORDS(geometry)
        GEOMETRY_DEDUPLICATE_XYZ(geometry)
        .def_property_readonly(
            "__geo_interface__",
            [](const mapbox::geojson::geometry &self) -> py::object {
                return to_python(self);
            })
        .def(
            "from_rapidjson",
            [](mapbox::geojson::geometry &self,
               const RapidjsonValue &json) -> mapbox::geojson::geometry & {
                self =
                    mapbox::geojson::convert<mapbox::geojson::geometry>(json);
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::geometry &self) {
                 RapidjsonAllocator allocator;
                 auto json = mapbox::geojson::convert(self, allocator);
                 return json;
             })
        .def(
            "from_geobuf",
            [](mapbox::geojson::geometry &self,
                const std::string &bytes) -> mapbox::geojson::geometry & {
                auto geojson = mapbox::geobuf::Decoder().decode(bytes);
                self = std::move(geojson.get<mapbox::geojson::geometry>());
                return self;
            },
            rvp::reference_internal)
        .def("to_geobuf",
            [](const mapbox::geojson::geometry &self, //
            int precision, bool only_xy, std::optional<int> round_z) {
            auto bytes =
                mapbox::geobuf::Encoder(std::pow(10, precision), only_xy, round_z)
                    .encode(self);
            return py::bytes(bytes);
            }, py::kw_only(), //
            "precision"_a = 8, //
            "only_xy"_a = false, //
            "round_z"_a = std::nullopt)
        .def("load",
            [](mapbox::geojson::geometry &self, const std::string &path) -> mapbox::geojson::geometry & {
                if (endswith(path, ".pbf")) {
                    auto bytes = mapbox::geobuf::load_bytes(path);
                    auto geojson = mapbox::geobuf::Decoder().decode(bytes);
                    self = std::move(geojson.get<mapbox::geojson::geometry>());
                    return self;
                }
                auto json = load_json(path);
                self =
                    mapbox::geojson::convert<mapbox::geojson::geometry>(json);
                return self;
            }, rvp::reference_internal)
        .def("dump",
            [](const mapbox::geojson::geometry &self, //
                const std::string &path, //
                bool indent, //
                bool sort_keys, //
                int precision, //
                bool only_xy) {
                if (endswith(path, ".pbf")) {
                    auto bytes = mapbox::geobuf::Encoder(std::pow(10, precision), only_xy).encode(self);
                    return mapbox::geobuf::dump_bytes(path, bytes);
                }
                RapidjsonAllocator allocator;
                auto json = mapbox::geojson::convert(self, allocator);
                sort_keys_inplace(json);
                return dump_json(path, json, indent);
            }, "path"_a, py::kw_only(), //
            "indent"_a = false, //
            "sort_keys"_a = false, //
            "precision"_a = 8, //
            "only_xy"_a = false)
        .def("bbox", [](const mapbox::geojson::geometry &self, bool with_z) -> Eigen::VectorXd {
            return geom2bbox(self, with_z);
        }, py::kw_only(), "with_z"_a = false)
        .def(py::self == py::self) //
        .def(py::self != py::self) //

        .def("__call__",
             [](const mapbox::geojson::geometry &self) {
                 return to_python(self);
             })
        //
        ;

    py::class_<mapbox::geojson::point>(geojson, "Point", py::module_local())
        .def(py::init<>())
        .def(py::init<double, double, double>(), "x"_a, "y"_a, "z"_a = 0.0)
        .def(py::init([](const Eigen::VectorXd &p) {
            return mapbox::geojson::point(p[0], p[1],
                                          p.size() > 2 ? p[2] : 0.0);
        }))
        .def(
            "as_numpy",
            [](mapbox::geojson::point &self) -> Eigen::Map<Eigen::Vector3d> {
                return Eigen::Vector3d::Map(&self.x);
            },
            rvp::reference_internal)
        .def("to_numpy",
             [](const mapbox::geojson::point &self) -> Eigen::Vector3d {
                 return Eigen::Vector3d::Map(&self.x);
             })
        .def(
            "from_numpy",
            [](mapbox::geojson::point &self,
               const Eigen::VectorXd &p) -> mapbox::geojson::point & {
                self.x = p[0];
                self.y = p[1];
                self.z = p.size() > 2 ? p[2] : 0.0;
                return self;
            },
            rvp::reference_internal)
        .def_property(
            "x", [](const mapbox::geojson::point &self) { return self.x; },
            [](mapbox::geojson::point &self, double value) { self.x = value; })
        .def_property(
            "y", [](const mapbox::geojson::point &self) { return self.y; },
            [](mapbox::geojson::point &self, double value) { self.y = value; })
        .def_property(
            "z", [](const mapbox::geojson::point &self) { return self.z; },
            [](mapbox::geojson::point &self, double value) { self.z = value; })
        .def(
            "__getitem__",
            [](mapbox::geojson::point &self, int index) -> double {
                return *(&self.x + (index >= 0 ? index : index + 3));
            },
            "index"_a)
        .def(
            "__setitem__",
            [](mapbox::geojson::point &self, int index, double v) {
                *(&self.x + (index >= 0 ? index : index + 3)) = v;
                return v;
            },
            "index"_a, "value"_a) //
        .def("__len__",
             [](const mapbox::geojson::point &self) -> int { return 3; })
        .def(
            "__iter__",
            [](mapbox::geojson::point &self) {
                return py::make_iterator(&self.x, &self.x + 3);
            },
            py::keep_alive<0, 1>())
        //
        copy_deepcopy_clone(mapbox::geojson::point)
        .def(py::pickle(
            [](const mapbox::geojson::point &self) {
                return to_python(mapbox::geojson::geometry(self));
            },
            [](py::object o) -> mapbox::geojson::point {
                auto json = to_rapidjson(o);
                return mapbox::geojson::convert<mapbox::geojson::geometry>(json)
                    .get<mapbox::geojson::point>();
            }))                         //
        GEOMETRY_ROUND_COORDS(point)    //
        GEOMETRY_DEDUPLICATE_XYZ(point) //
        .def_property_readonly(
            "__geo_interface__",
            [](const mapbox::geojson::point &self) -> py::object {
                return to_python(self);
            })
        .def(
            "from_rapidjson",
            [](mapbox::geojson::point &self,
               const RapidjsonValue &json) -> mapbox::geojson::point & {
                self = mapbox::geojson::convert<mapbox::geojson::geometry>(json)
                           .get<mapbox::geojson::point>();
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::point &self) {
                 RapidjsonAllocator allocator;
                 auto json = mapbox::geojson::convert(
                     mapbox::geojson::geometry{self}, allocator);
                 return json;
             })
        .def(
            "bbox",
            [](const mapbox::geojson::point &self, bool with_z)
                -> Eigen::VectorXd { return geom2bbox(self, with_z); },
            py::kw_only(), "with_z"_a = false)
        .def(py::self == py::self) //
        .def(py::self != py::self) //
        .def(
            "clear",
            [](mapbox::geojson::point &self)
                -> mapbox::geojson::point & { // more like "reset"
                self.x = 0.0;
                self.y = 0.0;
                self.z = 0.0;
                return self;
            },
            rvp::reference_internal)
        .def("__call__",
             [](const mapbox::geojson::point &self) { return to_python(self); })
        //
        ;

#define BIND_FOR_VECTOR_POINT_TYPE_PURE(geom_type)                             \
    .def("__call__",                                                           \
         [](const mapbox::geojson::geom_type &self) {                          \
             return to_python(self);                                           \
         })                                                                    \
        .def(                                                                  \
            "__getitem__",                                                     \
            [](mapbox::geojson::geom_type &self,                               \
               int index) -> mapbox::geojson::point & {                        \
                return self[index >= 0 ? index : index + (int)self.size()];    \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def("__setitem__",                                                    \
             [](mapbox::geojson::geom_type &self, int index,                   \
                const mapbox::geojson::point &p) {                             \
                 self[index >= 0 ? index : index + (int)self.size()] = p;      \
                 return p;                                                     \
             })                                                                \
        .def("__setitem__",                                                    \
             [](mapbox::geojson::geom_type &self, int index,                   \
                const Eigen::VectorXd &p) {                                    \
                 index = index >= 0 ? index : index + (int)self.size();        \
                 self[index].x = p[0];                                         \
                 self[index].y = p[1];                                         \
                 self[index].z = p.size() > 2 ? p[2] : 0.0;                    \
                 return p;                                                     \
             })                                                                \
        .def("__len__",                                                        \
             [](const mapbox::geojson::geom_type &self) -> int {               \
                 return self.size();                                           \
             })                                                                \
        .def(                                                                  \
            "__iter__",                                                        \
            [](mapbox::geojson::geom_type &self) {                             \
                return py::make_iterator(self.begin(), self.end());            \
            },                                                                 \
            py::keep_alive<0, 1>())                                            \
        .def(                                                                  \
            "clear",                                                           \
            [](mapbox::geojson::geom_type &self)                               \
                -> mapbox::geojson::geom_type & {                              \
                self.clear();                                                  \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "pop_back",                                                        \
            [](mapbox::geojson::geom_type &self)                               \
                -> mapbox::geojson::geom_type & {                              \
                self.pop_back();                                               \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "push_back",                                                       \
            [](mapbox::geojson::geom_type &self,                               \
               const mapbox::geojson::point &point)                            \
                -> mapbox::geojson::geom_type & {                              \
                self.push_back(point);                                         \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "push_back",                                                       \
            [](mapbox::geojson::geom_type &self,                               \
               const Eigen::VectorXd &xyz) -> mapbox::geojson::geom_type & {   \
                self.emplace_back(xyz[0], xyz[1],                              \
                                  xyz.size() > 2 ? xyz[2] : 0.0);              \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "as_numpy",                                                        \
            [](mapbox::geojson::geom_type &self) -> Eigen::Map<RowVectors> {   \
                return Eigen::Map<RowVectors>(&self[0].x, self.size(), 3);     \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def("to_numpy",                                                       \
             [](const mapbox::geojson::geom_type &self) -> RowVectors {        \
                 return Eigen::Map<const RowVectors>(&self[0].x, self.size(),  \
                                                     3);                       \
             })                                                                \
        .def(                                                                  \
            "from_numpy",                                                      \
            [](mapbox::geojson::geom_type &self,                               \
               const Eigen::Ref<const MatrixXdRowMajor> &points)               \
                -> mapbox::geojson::geom_type & {                              \
                eigen2geom(points, self);                                      \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
            copy_deepcopy_clone(mapbox::geojson::geom_type) //

#define BIND_FOR_VECTOR_POINT_TYPE(geom_type)                                  \
    BIND_FOR_VECTOR_POINT_TYPE_PURE(geom_type)                                 \
        .def(py::init([](const Eigen::Ref<const MatrixXdRowMajor> &points) {   \
            mapbox::geojson::geom_type self;                                   \
            eigen2geom(points, self);                                          \
            return self;                                                       \
        }))                                                                    \
        .def("resize",                                                         \
             [](mapbox::geojson::geom_type &self,                              \
                int size) -> mapbox::geojson::geom_type & {                    \
                 self.resize(size);                                            \
                 return self;                                                  \
             })                                                                \
        .def(py::pickle(                                                       \
            [](const mapbox::geojson::geom_type &self) {                       \
                return to_python(mapbox::geojson::geometry{self});             \
            },                                                                 \
            [](py::object o) -> mapbox::geojson::geom_type {                   \
                auto json = to_rapidjson(o);                                   \
                return mapbox::geojson::convert<mapbox::geojson::geometry>(    \
                           json)                                               \
                    .get<mapbox::geojson::geom_type>();                        \
            })) GEOMETRY_ROUND_COORDS(geom_type)                               \
            GEOMETRY_DEDUPLICATE_XYZ(geom_type)                                \
        .def_property_readonly(                                                \
            "__geo_interface__",                                               \
            [](const mapbox::geojson::geom_type &self) -> py::object {         \
                return to_python(mapbox::geojson::geometry(self));             \
            })                                                                 \
        .def(                                                                  \
            "from_rapidjson",                                                  \
            [](mapbox::geojson::geom_type &self,                               \
               const RapidjsonValue &json) -> mapbox::geojson::geom_type & {   \
                self =                                                         \
                    mapbox::geojson::convert<mapbox::geojson::geometry>(json)  \
                        .get<mapbox::geojson::geom_type>();                    \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def("to_rapidjson",                                                   \
             [](const mapbox::geojson::geom_type &self) {                      \
                 RapidjsonAllocator allocator;                                 \
                 auto json = mapbox::geojson::convert(                         \
                     mapbox::geojson::geometry{self}, allocator);              \
                 return json;                                                  \
             })                                                                \
        .def(                                                                  \
            "bbox",                                                            \
            [](const mapbox::geojson::geom_type &self, bool with_z)            \
                -> Eigen::VectorXd { return geom2bbox(self, with_z); },        \
            py::kw_only(), "with_z"_a = false)

    py::class_<mapbox::geojson::multi_point,
               std::vector<mapbox::geojson::point>>(geojson, "MultiPoint",
                                                    py::module_local())
        .def(py::init<>())                      //
        BIND_FOR_VECTOR_POINT_TYPE(multi_point) //
        .def(py::self == py::self)              //
        .def(py::self != py::self)              //
        //
        ;
    py::class_<mapbox::geojson::line_string,
               std::vector<mapbox::geojson::point>>(geojson, "LineString",
                                                    py::module_local())
        .def(py::init<>())                      //
        BIND_FOR_VECTOR_POINT_TYPE(line_string) //
        .def(py::self == py::self)              //
        .def(py::self != py::self)              //
        .def("deduplicate_xyz",
             [](mapbox::geojson::line_string &self) {
                 return deduplicate_xyz(self);
             })
        //
        ;

#define BIND_FOR_VECTOR_LINEAR_RING_TYPE(geom_type)                            \
    .def(py::init([](const Eigen::Ref<const MatrixXdRowMajor> &points) {       \
        mapbox::geojson::geom_type self;                                       \
        eigen2geom(points, self);                                              \
        return self;                                                           \
    }))                                                                        \
        .def("__call__",                                                       \
             [](const mapbox::geojson::geom_type &self) {                      \
                 return to_python(self);                                       \
             })                                                                \
        .def("__len__",                                                        \
             [](const mapbox::geojson::geom_type &self) -> int {               \
                 return self.size();                                           \
             })                                                                \
        .def(                                                                  \
            "__iter__",                                                        \
            [](mapbox::geojson::geom_type &self) {                             \
                return py::make_iterator(self.begin(), self.end());            \
            },                                                                 \
            py::keep_alive<0, 1>())                                            \
        .def(                                                                  \
            "__getitem__",                                                     \
            [](mapbox::geojson::geom_type &self,                               \
               int index) -> decltype(self[0]) & {                             \
                return self[index >= 0 ? index : index + (int)self.size()];    \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def("__setitem__",                                                    \
             [](mapbox::geojson::geom_type &self, int index,                   \
                const Eigen::Ref<const MatrixXdRowMajor> &points) {            \
                 auto &g =                                                     \
                     self[index >= 0 ? index : index + (int)self.size()];      \
                 eigen2geom(points, g);                                        \
                 return points;                                                \
             })                                                                \
        .def(                                                                  \
            "clear",                                                           \
            [](mapbox::geojson::geom_type &self)                               \
                -> mapbox::geojson::geom_type & {                              \
                self.clear();                                                  \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "pop_back",                                                        \
            [](mapbox::geojson::geom_type &self)                               \
                -> mapbox::geojson::geom_type & {                              \
                self.back().pop_back();                                        \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "push_back",                                                       \
            [](mapbox::geojson::geom_type &self,                               \
               const Eigen::Ref<const MatrixXdRowMajor> &points)               \
                -> mapbox::geojson::geom_type & {                              \
                mapbox::geojson::geom_type::container_type::value_type ls;     \
                eigen2geom(points, ls);                                        \
                self.push_back(ls);                                            \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "push_back",                                                       \
            [](mapbox::geojson::geom_type &self,                               \
               const mapbox::geojson::geom_type::container_type::value_type    \
                   &g) -> mapbox::geojson::geom_type & {                       \
                self.push_back(g);                                             \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def(                                                                  \
            "as_numpy",                                                        \
            [](mapbox::geojson::geom_type &self) -> Eigen::Map<RowVectors> {   \
                return as_row_vectors(self);                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def("to_numpy",                                                       \
             [](const mapbox::geojson::geom_type &self) -> RowVectors {        \
                 return as_row_vectors(self);                                  \
             })                                                                \
        .def(                                                                  \
            "from_numpy",                                                      \
            [](mapbox::geojson::geom_type &self,                               \
               const Eigen::Ref<const MatrixXdRowMajor> &points)               \
                -> mapbox::geojson::geom_type & {                              \
                eigen2geom(points, self);                                      \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
            copy_deepcopy_clone(mapbox::geojson::geom_type)                    \
        .def(py::pickle(                                                       \
            [](const mapbox::geojson::geom_type &self) {                       \
                return to_python(mapbox::geojson::geometry{self});             \
            },                                                                 \
            [](py::object o) -> mapbox::geojson::geom_type {                   \
                auto json = to_rapidjson(o);                                   \
                return mapbox::geojson::convert<mapbox::geojson::geometry>(    \
                           json)                                               \
                    .get<mapbox::geojson::geom_type>();                        \
            }))                                                                \
        .def_property_readonly(                                                \
            "__geo_interface__",                                               \
            [](const mapbox::geojson::geom_type &self) -> py::object {         \
                return to_python(mapbox::geojson::geometry(self));             \
            })                                                                 \
        .def(                                                                  \
            "from_rapidjson",                                                  \
            [](mapbox::geojson::geom_type &self,                               \
               const RapidjsonValue &json) -> mapbox::geojson::geom_type & {   \
                self =                                                         \
                    mapbox::geojson::convert<mapbox::geojson::geometry>(json)  \
                        .get<mapbox::geojson::geom_type>();                    \
                return self;                                                   \
            },                                                                 \
            rvp::reference_internal)                                           \
        .def("to_rapidjson",                                                   \
             [](const mapbox::geojson::geom_type &self) {                      \
                 RapidjsonAllocator allocator;                                 \
                 auto json = mapbox::geojson::convert(                         \
                     mapbox::geojson::geometry{self}, allocator);              \
                 return json;                                                  \
             })                                                                \
        .def(                                                                  \
            "round",                                                           \
            [](mapbox::geojson::geom_type &self, int lon, int lat,             \
               int alt) -> mapbox::geojson::geom_type & {                      \
                for (auto &g : self) {                                         \
                    round_coords(g, lon, lat, alt);                            \
                }                                                              \
                return self;                                                   \
            },                                                                 \
            py::kw_only(), "lon"_a = 8, "lat"_a = 8, "alt"_a = 3,              \
            rvp::reference_internal) GEOMETRY_DEDUPLICATE_XYZ(geom_type)       \
        .def(                                                                  \
            "bbox",                                                            \
            [](const mapbox::geojson::geom_type &self, bool with_z)            \
                -> Eigen::VectorXd { return geom2bbox(self, with_z); },        \
            py::kw_only(), "with_z"_a = false)

    py::class_<mapbox::geojson::linear_ring,
               mapbox::geojson::linear_ring::container_type>(
        geojson, "LinearRing", py::module_local()) //
        .def(py::init<>())                         //
        BIND_FOR_VECTOR_POINT_TYPE_PURE(linear_ring)
        .def(py::self == py::self) //
        .def(py::self != py::self) //
        //
        ;

    py::bind_vector<mapbox::geojson::multi_line_string::container_type>(
        geojson, "LineStringList", py::module_local());

    py::class_<mapbox::geojson::multi_line_string,
               mapbox::geojson::multi_line_string::container_type>(
        geojson, "MultiLineString", py::module_local()) //
        .def(py::init<>())
        .def(py::init<mapbox::geojson::multi_line_string::container_type>())
        .def(py::init([](std::vector<mapbox::geojson::point> line_string) {
            return mapbox::geojson::multi_line_string({std::move(line_string)});
        })) //
        //
        BIND_FOR_VECTOR_LINEAR_RING_TYPE(multi_line_string) //
        .def(py::self == py::self)                          //
        .def(py::self != py::self)                          //
        //
        ;

    py::bind_vector<mapbox::geojson::polygon::container_type>(
        geojson, "LinearRingList", py::module_local());
    py::class_<mapbox::geojson::polygon,
               mapbox::geojson::polygon::container_type>(geojson, "Polygon",
                                                         py::module_local()) //
        .def(py::init<>())
        .def(py::init<mapbox::geojson::polygon::container_type>())
        .def(py::init([](std::vector<mapbox::geojson::point> shell) {
            return mapbox::geojson::polygon({std::move(shell)});
        })) //
        //
        BIND_FOR_VECTOR_LINEAR_RING_TYPE(polygon) //
        .def(py::self == py::self)                //
        .def(py::self != py::self)                //
        //
        ;

    py::bind_vector<mapbox::geojson::multi_polygon::container_type>(
        geojson, "PolygonList");
    py::class_<mapbox::geojson::multi_polygon,
               mapbox::geojson::multi_polygon::container_type>(
        geojson, "MultiPolygon", py::module_local()) //
        .def(py::init<>())
        .def(py::init<mapbox::geojson::multi_polygon>())
        .def(py::init<mapbox::geojson::multi_polygon::container_type>())
        .def(py::init([](const Eigen::Ref<const MatrixXdRowMajor> &points) {
            mapbox::geojson::multi_polygon self;
            eigen2geom(points, self);
            return self;
        }))
        .def(
            "as_numpy",
            [](mapbox::geojson::multi_polygon &self) -> Eigen::Map<RowVectors> {
                return as_row_vectors(self);
            },
            rvp::reference_internal)
        .def("to_numpy",
             [](const mapbox::geojson::polygon &self) -> RowVectors {
                 return as_row_vectors(self);
             }) //
        .def(
            "from_numpy",
            [](mapbox::geojson::multi_polygon &self,
               const Eigen::Ref<const MatrixXdRowMajor> &points)
                -> mapbox::geojson::multi_polygon & {
                eigen2geom(points, self);
                return self;
            },
            rvp::reference_internal) //
                                     //
        .def("__call__",
             [](const mapbox::geojson::multi_polygon &self) {
                 return to_python(self);
             })
        .def("__len__",
             [](const mapbox::geojson::multi_polygon &self) -> int {
                 return self.size();
             })
        .def(
            "__iter__",
            [](mapbox::geojson::multi_polygon &self) {
                return py::make_iterator(self.begin(), self.end());
            },
            py::keep_alive<0, 1>())
        .def(
            "__getitem__",
            [](mapbox::geojson::multi_polygon &self,
               int index) -> mapbox::geojson::polygon & {
                return self[index >= 0 ? index : index + (int)self.size()];
            },
            rvp::reference_internal)
        .def("__setitem__",
             [](mapbox::geojson::multi_polygon &self, int index,
                const mapbox::geojson::polygon &polygon) {
                 self[index >= 0 ? index : index + (int)self.size()] = polygon;
                 return polygon;
             })
        .def("__setitem__",
             [](mapbox::geojson::multi_polygon &self, int index,
                const Eigen::Ref<const MatrixXdRowMajor> &points) {
                 auto &polygon =
                     self[index >= 0 ? index : index + (int)self.size()];
                 eigen2geom(points, polygon);
                 return polygon;
             })
        .def(
            "clear",
            [](mapbox::geojson::multi_polygon &self)
                -> mapbox::geojson::multi_polygon & {
                self.clear();
                return self;
            },
            rvp::reference_internal)
        .def(
            "pop_back",
            [](mapbox::geojson::multi_polygon &self)
                -> mapbox::geojson::multi_polygon & {
                self.pop_back();
                return self;
            },
            rvp::reference_internal)
        .def(
            "push_back",
            [](mapbox::geojson::multi_polygon &self,
               const Eigen::Ref<const MatrixXdRowMajor> &points)
                -> mapbox::geojson::multi_polygon & {
                mapbox::geojson::polygon polygon;
                eigen2geom(points, polygon);
                self.push_back(std::move(polygon));
                return self;
            },
            rvp::reference_internal)
        .def(
            "push_back",
            [](mapbox::geojson::multi_polygon &self,
               const mapbox::geojson::polygon &polygon)
                -> mapbox::geojson::multi_polygon & {
                self.push_back(polygon);
                return self;
            },
            rvp::reference_internal)
            copy_deepcopy_clone(mapbox::geojson::multi_polygon)
        .def(py::pickle(
            [](const mapbox::geojson::multi_polygon &self) {
                return to_python(mapbox::geojson::geometry{self});
            },
            [](py::object o) -> mapbox::geojson::multi_polygon {
                auto json = to_rapidjson(o);
                return mapbox::geojson::convert<mapbox::geojson::geometry>(json)
                    .get<mapbox::geojson::multi_polygon>();
            }))
        .def(
            "round",
            [](mapbox::geojson::multi_polygon &self, int lon, int lat,
               int alt) -> mapbox::geojson::multi_polygon & {
                for (auto &gg : self) {
                    for (auto &g : gg) {
                        round_coords(g, lon, lat, alt);
                    }
                }
                return self;
            },
            py::kw_only(), "lon"_a = 8, "lat"_a = 8, "alt"_a = 3,
            rvp::reference_internal)
        .def_property_readonly(
            "__geo_interface__",
            [](const mapbox::geojson::multi_polygon &self) -> py::object {
                return to_python(mapbox::geojson::geometry(self));
            })
        .def(
            "from_rapidjson",
            [](mapbox::geojson::multi_polygon &self,
               const RapidjsonValue &json) -> mapbox::geojson::multi_polygon & {
                self = mapbox::geojson::convert<mapbox::geojson::geometry>(json)
                           .get<mapbox::geojson::multi_polygon>();
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::multi_polygon &self) {
                 RapidjsonAllocator allocator;
                 auto json = mapbox::geojson::convert(
                     mapbox::geojson::geometry{self}, allocator);
                 return json;
             })
        .def(
            "bbox",
            [](const mapbox::geojson::multi_polygon &self, bool with_z)
                -> Eigen::VectorXd { return geom2bbox(self, with_z); },
            py::kw_only(), "with_z"_a = false)
        .def(py::self == py::self) //
        .def(py::self != py::self) //
        //
        ;

    py::bind_vector<mapbox::geojson::geometry_collection::container_type>(
        geojson, "GeometryList", py::module_local());
    py::class_<mapbox::geojson::geometry_collection,
               mapbox::geojson::geometry_collection::container_type>(
        geojson, "GeometryCollection", py::module_local()) //
        .def(py::init<>())
        .def(py::init(
            [](const mapbox::geojson::geometry_collection &g) { return g; }))
        .def(py::init(
                 [](int N) { return mapbox::geojson::geometry_collection(N); }),
             "N"_a)
        .def(
            "resize",
            [](mapbox::geojson::geometry_collection &self,
               int N) -> mapbox::geojson::geometry_collection & {
                self.resize(N);
                return self;
            },
            rvp::reference_internal)
#define SETITEM_FOR_TYPE(geom_type)                                            \
    .def(                                                                      \
        "__setitem__",                                                         \
        [](mapbox::geojson::geometry_collection &self, int index,              \
           const mapbox::geojson::geom_type &g) {                              \
            self[index >= 0 ? index : index + (int)self.size()] = g;           \
            return self;                                                       \
        },                                                                     \
        rvp::reference_internal)
        //
        SETITEM_FOR_TYPE(geometry)            //
        SETITEM_FOR_TYPE(point)               //
        SETITEM_FOR_TYPE(multi_point)         //
        SETITEM_FOR_TYPE(line_string)         //
        SETITEM_FOR_TYPE(multi_line_string)   //
        SETITEM_FOR_TYPE(polygon)             //
        SETITEM_FOR_TYPE(multi_polygon)       //
        SETITEM_FOR_TYPE(geometry_collection) //
#undef SETITEM_FOR_TYPE
        .def(
            "clear",
            [](mapbox::geojson::geometry_collection &self)
                -> mapbox::geojson::geometry_collection & {
                self.clear();
                return self;
            },
            rvp::reference_internal)
        .def(
            "pop_back",
            [](mapbox::geojson::geometry_collection &self)
                -> mapbox::geojson::geometry_collection & {
                self.pop_back();
                return self;
            },
            rvp::reference_internal)
#define PUSH_BACK_FOR_TYPE(geom_type)                                          \
    .def(                                                                      \
        "push_back",                                                           \
        [](mapbox::geojson::geometry_collection &self,                         \
           const mapbox::geojson::geom_type &g) {                              \
            self.push_back(g);                                                 \
            return self;                                                       \
        },                                                                     \
        rvp::reference_internal)
        //
        PUSH_BACK_FOR_TYPE(geometry)            //
        PUSH_BACK_FOR_TYPE(point)               //
        PUSH_BACK_FOR_TYPE(multi_point)         //
        PUSH_BACK_FOR_TYPE(line_string)         //
        PUSH_BACK_FOR_TYPE(multi_line_string)   //
        PUSH_BACK_FOR_TYPE(polygon)             //
        PUSH_BACK_FOR_TYPE(multi_polygon)       //
        PUSH_BACK_FOR_TYPE(geometry_collection) //
#undef PUSH_BACK_FOR_TYPE
        .def(py::pickle(
            [](const mapbox::geojson::geometry_collection &self) {
                return to_python(mapbox::geojson::geometry{self});
            },
            [](py::object o) -> mapbox::geojson::geometry_collection {
                auto json = to_rapidjson(o);
                return mapbox::geojson::convert<mapbox::geojson::geometry>(json)
                    .get<mapbox::geojson::geometry_collection>();
            }))
        .def(
            "round",
            [](mapbox::geojson::geometry_collection &self, int lon, int lat,
               int alt) -> mapbox::geojson::geometry_collection & {
                for (auto &g : self) {
                    round_coords(g, lon, lat, alt);
                }
                return self;
            },
            py::kw_only(), "lon"_a = 8, "lat"_a = 8, "alt"_a = 3,
            rvp::reference_internal)
            GEOMETRY_DEDUPLICATE_XYZ(geometry_collection)
        .def_property_readonly(
            "__geo_interface__",
            [](const mapbox::geojson::geometry_collection &self) -> py::object {
                return to_python(mapbox::geojson::geometry(self));
            })
        .def(
            "from_rapidjson",
            [](mapbox::geojson::geometry_collection &self,
               const RapidjsonValue &json)
                -> mapbox::geojson::geometry_collection & {
                self = mapbox::geojson::convert<mapbox::geojson::geometry>(json)
                           .get<mapbox::geojson::geometry_collection>();
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::geometry_collection &self) {
                 RapidjsonAllocator allocator;
                 auto json = mapbox::geojson::convert(
                     mapbox::geojson::geometry{self}, allocator);
                 return json;
             })
        .def("__call__",
             [](const mapbox::geojson::geometry_collection &self) {
                 return to_python(self);
             })
        .def(py::self == py::self) //
        .def(py::self != py::self) //
        ;

    auto geojson_value =
        py::class_<mapbox::geojson::value>(geojson, "value", py::module_local())
            .def(py::init<>())
            .def(
                py::init([](const py::object &obj) { return to_geojson_value(obj); }))
            .def("GetType",
                 [](const mapbox::geojson::value &self) {
                    return get_type(self);
                 })
            .def("__call__",
                 [](const mapbox::geojson::value &self) {
                     return to_python(self);
                 })
            .def("Get",
                 [](const mapbox::geojson::value &self) {
                     return to_python(self);
                 })
            .def("GetBool",
                 [](mapbox::geojson::value &self) { return self.get<bool>(); })
            .def("GetUint64",
                 [](mapbox::geojson::value &self) {
                     return self.get<uint64_t>();
                 })
            .def("GetInt64",
                 [](mapbox::geojson::value &self) {
                     return self.get<int64_t>();
                 })
            .def("GetDouble",
                 [](mapbox::geojson::value &self) -> double & {
                     return self.get<double>();
                 })
            .def("GetString",
                 [](mapbox::geojson::value &self) -> std::string & {
                     return self.get<std::string>();
                 })
            // casters
            .def("is_object",
                 [](const mapbox::geojson::value &self) {
                     return self.is<mapbox::geojson::value::object_type>();
                 })
            .def("as_object",
                 [](mapbox::geojson::value &self)
                     -> mapbox::geojson::value::object_type & {
                         return self.get<mapbox::geojson::value::object_type>();
                     },
                 rvp::reference_internal)
            .def("is_array",
                 [](const mapbox::geojson::value &self) {
                     return self.is<mapbox::geojson::value::array_type>();
                 })
            .def("as_array",
                 [](mapbox::geojson::value &self)
                     -> mapbox::geojson::value::array_type & {
                         return self.get<mapbox::geojson::value::array_type>();
                     },
                 rvp::reference_internal)
            .def("__getitem__",
                 [](mapbox::geojson::value &self,
                    int index) -> mapbox::geojson::value & {
                     auto &arr = self.get<mapbox::geojson::value::array_type>();
                     return arr[index >= 0 ? index : index + (int)arr.size()];
                 },
                 rvp::reference_internal)
            .def("__getitem__",
                 [](mapbox::geojson::value &self,
                    const std::string &key) -> mapbox::geojson::value & {
                     auto &obj =
                         self.get<mapbox::geojson::value::object_type>();
                     return obj.at(key);
                 },
                 rvp::reference_internal)                         //
            .def(
                "get", // get by key
                [](mapbox::geojson::value &self,
                    const std::string &key) -> mapbox::geojson::value * {
                     auto &obj =
                         self.get<mapbox::geojson::value::object_type>();
                    auto itr = obj.find(key);
                    if (itr == obj.end()) {
                        return nullptr;
                    }
                    return &itr->second;
                },
                "key"_a, rvp::reference_internal)
            .def("set", // set value
                 [](mapbox::geojson::value &self,
                    const py::object &obj) -> mapbox::geojson::value & {
                     self = to_geojson_value(obj);
                     return self;
                 },
                 rvp::reference_internal)
            .def("__setitem__",
                 [](mapbox::geojson::value &self, const std::string &key,
                    const py::object &value) {
                     auto &obj =
                         self.get<mapbox::geojson::value::object_type>();
                     obj[key] = to_geojson_value(value);
                     return value;
                 })
            .def("__setitem__",
                 [](mapbox::geojson::value &self, int index,
                    const py::object &value) {
                     auto &arr = self.get<mapbox::geojson::value::array_type>();
                     arr[index >= 0 ? index : index + (int)arr.size()] =
                         to_geojson_value(value);
                     return value;
                 })
            .def("keys",
                 [](mapbox::geojson::value &self) {
                     std::vector<std::string> keys;
                     auto &obj =
                         self.get<mapbox::geojson::value::object_type>();
                     return py::make_key_iterator(obj);
                 }, py::keep_alive<0, 1>())
            .def("values",
                 [](mapbox::geojson::value &self) {
                     std::vector<std::string> keys;
                     auto &obj =
                         self.get<mapbox::geojson::value::object_type>();
                     return py::make_value_iterator(obj);
                 }, py::keep_alive<0, 1>())
            .def("items",
                 [](mapbox::geojson::value &self) {
                     auto &obj =
                         self.get<mapbox::geojson::value::object_type>();
                     return py::make_iterator(obj.begin(), obj.end());
                 },
                 py::keep_alive<0, 1>())

            .def("__delitem__",
                 [](mapbox::geojson::value &self, const std::string &key) {
                     auto &obj =
                         self.get<mapbox::geojson::value::object_type>();
                     return obj.erase(key);
                 })
            .def("__delitem__",
                 [](mapbox::geojson::value &self, int index) {
                     auto &arr = self.get<mapbox::geojson::value::array_type>();
                     arr.erase(arr.begin() +
                               (index >= 0 ? index : index + (int)arr.size()));
                 })
            .def("clear",
                 [](mapbox::geojson::value &self) -> mapbox::geojson::value & {
                     geojson_value_clear(self);
                     return self;
                 },
                 rvp::reference_internal)
            .def("push_back",
                 [](mapbox::geojson::value &self,
                    const py::object &value) -> mapbox::geojson::value & {
                     auto &arr = self.get<mapbox::geojson::value::array_type>();
                     arr.push_back(to_geojson_value(value));
                     return self;
                 },
                 rvp::reference_internal)
            .def("pop_back",
                 [](mapbox::geojson::value &self) -> mapbox::geojson::value & {
                     auto &arr = self.get<mapbox::geojson::value::array_type>();
                     arr.pop_back();
                     return self;
                 },
                 rvp::reference_internal)
            .def("__len__",
                 [](const mapbox::geojson::value &self) -> int {
                    return __len__(self);
                 })
            .def("__bool__",
                 [](const mapbox::geojson::value &self) -> bool {
                    return __bool__(self);
                 })
            .def(
                "from_rapidjson",
                [](mapbox::geojson::value &self, const RapidjsonValue &json) -> mapbox::geojson::value & {
                    self = mapbox::geojson::convert<mapbox::geojson::value>(json);
                    return self;
                },
                rvp::reference_internal)
            .def("to_rapidjson",
                [](const mapbox::geojson::value &self) {
                    return to_rapidjson(self);
                })
        //
        //
        ;

    py::bind_vector<mapbox::geojson::value::array_type>(
        geojson_value, "array_type", py::module_local())
        .def(py::init<>())
        .def(py::init([](const py::handle &arr) {
            return to_geojson_value(arr)
                .get<mapbox::geojson::value::array_type>();
        }))
        .def(
            "clear",
            [](mapbox::geojson::value::array_type &self)
                -> mapbox::geojson::value::array_type & {
                self.clear();
                return self;
            },
            rvp::reference_internal)
        .def(
            "__getitem__",
            [](mapbox::geojson::value::array_type &self,
               int index) -> mapbox::geojson::value & {
                return self[index >= 0 ? index : index + (int)self.size()];
            },
            rvp::reference_internal)
        .def(
            "__setitem__",
            [](mapbox::geojson::value::array_type &self, int index,
               const py::object &obj) {
                index = index < 0 ? index + (int)self.size() : index;
                self[index] = to_geojson_value(obj);
                return self[index]; // why not return obj?
            },
            rvp::reference_internal)
        .def(
            "from_rapidjson",
            [](mapbox::geojson::value::array_type &self,
               const RapidjsonValue &json)
                -> mapbox::geojson::value::array_type & {
                self = mapbox::geojson::convert<mapbox::geojson::value>(json)
                           .get<mapbox::geojson::value::array_type>();
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::value::array_type &self) {
                 return to_rapidjson(self);
             })
        .def("__call__",
             [](const mapbox::geojson::value::array_type &self) {
                 return to_python(self);
             })
        //
        ;

    py::bind_map<mapbox::geojson::value::object_type>(
        geojson_value, "object_type", py::module_local())
        .def(py::init<>())
        .def(py::init([](const py::object &obj) {
            return to_geojson_value(obj)
                .get<mapbox::geojson::value::object_type>();
        }))
        .def(
            "clear",
            [](mapbox::geojson::value::object_type &self)
                -> mapbox::geojson::value::object_type & {
                self.clear();
                return self;
            },
            rvp::reference_internal)
        .def(
            "__setitem__",
            [](mapbox::geojson::value::object_type &self,
               const std::string &key, const py::object &obj) {
                self[key] = to_geojson_value(obj);
                return self[key];
            },
            rvp::reference_internal)
        .def(
            "keys",
            [](const mapbox::geojson::value::object_type &self) {
                return py::make_key_iterator(self.begin(), self.end());
            },
            py::keep_alive<0, 1>())
        .def(
            "values",
            [](const mapbox::geojson::value::object_type &self) {
                return py::make_value_iterator(self.begin(), self.end());
            },
            py::keep_alive<0, 1>())
        .def(
            "items",
            [](mapbox::geojson::value::object_type &self) {
                return py::make_iterator(self.begin(), self.end());
            },
            py::keep_alive<0, 1>())
        .def(
            "from_rapidjson",
            [](mapbox::geojson::value::object_type &self,
               const RapidjsonValue &json)
                -> mapbox::geojson::value::object_type & {
                self = mapbox::geojson::convert<
                    mapbox::geojson::value::object_type>(json);
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::value::object_type &self) {
                 return to_rapidjson(self);
             })
        .def("__call__",
             [](const mapbox::geojson::value::object_type &self) {
                 return to_python(self);
             })
        //
        ;

    py::class_<mapbox::geojson::feature>(geojson, "Feature", py::module_local())
        .def(py::init<>())
        .def(py::init(
            [](const mapbox::geojson::feature &other) { return other; }))
        .def(py::init([](const RapidjsonValue &feature) {
            return mapbox::geojson::convert<mapbox::geojson::feature>(feature);
        }))
        .def(py::init([](const py::dict &feature) {
            auto json = to_rapidjson(feature);
            return mapbox::geojson::convert<mapbox::geojson::feature>(json);
        }))
        //
        BIND_PY_FLUENT_ATTRIBUTE(mapbox::geojson::feature,  //
                                 mapbox::geojson::geometry, //
                                 geometry)                  //
        BIND_PY_FLUENT_ATTRIBUTE(mapbox::geojson::feature,  //
                                 PropertyMap,               //
                                 properties)                //
        BIND_PY_FLUENT_ATTRIBUTE(mapbox::geojson::feature,  //
                                 PropertyMap,               //
                                 custom_properties)         //

// geometry from point, mulipoint, etc
#define GeometryFromType(geom_type)                                            \
    .def(                                                                      \
        "geometry",                                                            \
        [](mapbox::geojson::feature &self,                                     \
           const mapbox::geojson::geom_type &geometry)                         \
            -> mapbox::geojson::feature & {                                    \
            self.geometry = geometry;                                          \
            return self;                                                       \
        },                                                                     \
        #geom_type##_a, rvp::reference_internal) //
                                                 //
        GeometryFromType(point)                  //
        GeometryFromType(multi_point)            //
        GeometryFromType(line_string)            //
        GeometryFromType(multi_line_string)      //
        GeometryFromType(polygon)                //
        GeometryFromType(multi_polygon)          //
#undef GeometryFromType

        .def(
            "geometry",
            [](mapbox::geojson::feature &self,
               const py::object &obj) -> mapbox::geojson::feature & {
                auto json = to_rapidjson(obj);
                self.geometry =
                    mapbox::geojson::convert<mapbox::geojson::geometry>(json);
                return self;
            },
            rvp::reference_internal)
        .def(
            "properties",
            [](mapbox::geojson::feature &self,
               const py::object &obj) -> mapbox::geojson::feature & {
                auto json = to_rapidjson(obj);
                self.properties =
                    mapbox::geojson::convert<mapbox::feature::property_map>(
                        json);
                return self;
            },
            rvp::reference_internal)
        .def(
            "properties",
            [](mapbox::geojson::feature &self,
               const std::string &key) -> mapbox::geojson::value * {
                auto &props = self.properties;
                auto itr = props.find(key);
                if (itr == props.end()) {
                    return nullptr;
                }
                return &itr->second;
            },
            rvp::reference_internal)
        .def(
            "properties",
            [](mapbox::geojson::feature &self, const std::string &key,
               const py::object &value) -> mapbox::geojson::feature & {
                if (value.ptr() == nullptr || value.is_none()) {
                    self.properties.erase(key);
                } else {
                    self.properties[key] = to_geojson_value(value);
                }
                return self;
            },
            rvp::reference_internal)
        .def("id",
             [](mapbox::geojson::feature &self) { return to_python(self.id); })
        .def(
            "id",
            [](mapbox::geojson::feature &self,
               const py::object &value) -> mapbox::geojson::feature & {
                self.id = to_feature_id(value);
                return self;
            },
            rvp::reference_internal)
        //
        .def(
            "__getitem__",
            [](mapbox::geojson::feature &self,
               const std::string &key) -> mapbox::geojson::value * {
                // don't try "type", "geometry", "properties", "id"
                auto &props = self.custom_properties;
                auto itr = props.find(key);
                if (itr == props.end()) {
                    return nullptr;
                }
                return &itr->second;
            },
            rvp::reference_internal)
        .def("__setitem__",
             [](mapbox::geojson::feature &self, const std::string &key,
                const py::object &value) {
                 if (key == "type" || key == "geometry" ||
                     key == "properties" || key == "id") {
                     throw pybind11::key_error(key);
                 }
                 self.custom_properties[key] = to_geojson_value(value);
                 return value;
             })
        .def("__delitem__",
             [](mapbox::geojson::feature &self, const std::string &key) {
                 return self.custom_properties.erase(key);
             })
        .def(
            "keys",
            [](mapbox::geojson::feature &self) {
                return py::make_key_iterator(self.custom_properties);
            },
            py::keep_alive<0, 1>())
        .def(
            "items",
            [](mapbox::geojson::feature &self) {
                return py::make_iterator(self.custom_properties.begin(),
                                         self.custom_properties.end());
            },
            py::keep_alive<0, 1>())
        .def(
            "clear",
            [](mapbox::geojson::feature &self) -> mapbox::geojson::feature & {
                geometry_clear(self.geometry);
                self.geometry.custom_properties.clear();
                self.properties.clear();
                self.id = mapbox::geojson::null_value_t();
                self.custom_properties.clear();
                return self;
            },
            rvp::reference_internal)
        .def(
            "bbox",
            [](const mapbox::geojson::feature &self, bool with_z)
                -> Eigen::VectorXd { return geom2bbox(self.geometry, with_z); },
            py::kw_only(), "with_z"_a = false)
        .def(py::self == py::self) //
        .def(py::self != py::self) //
        //
        .def(
            "as_numpy",
            [](mapbox::geojson::feature &self) -> Eigen::Map<RowVectors> {
                return as_row_vectors(self.geometry);
            },
            rvp::reference_internal)
        .def("to_numpy",
             [](const mapbox::geojson::feature &self) -> RowVectors {
                 return as_row_vectors(self.geometry);
             }) //
        .def("__call__",
             [](const mapbox::geojson::feature &self) {
                 return to_python(self);
             })
        .def(
            "from_rapidjson",
            [](mapbox::geojson::feature &self,
               const RapidjsonValue &json) -> mapbox::geojson::feature & {
                self = mapbox::geojson::convert<mapbox::geojson::feature>(json);
                return self;
            },
            rvp::reference_internal)
        .def(
            "from_rapidjson",
            [](mapbox::geojson::feature &self,
               const py::object &feature) -> mapbox::geojson::feature & {
                self = mapbox::geojson::convert<mapbox::geojson::feature>(
                    to_rapidjson(feature));
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::feature &self) {
                 RapidjsonAllocator allocator;
                 return mapbox::geojson::convert(self, allocator);
             })
        .def(
            "from_geobuf",
            [](mapbox::geojson::feature &self,
               const std::string &bytes) -> mapbox::geojson::feature & {
                auto geojson = mapbox::geobuf::Decoder().decode(bytes);
                self = std::move(geojson.get<mapbox::geojson::feature>());
                return self;
            },
            rvp::reference_internal)
        .def(
            "to_geobuf",
            [](const mapbox::geojson::feature &self, //
               int precision, bool only_xy, std::optional<int> round_z) {
                auto bytes = mapbox::geobuf::Encoder(std::pow(10, precision),
                                                     only_xy, round_z)
                                 .encode(self);
                return py::bytes(bytes);
            },
            py::kw_only(),       //
            "precision"_a = 8,   //
            "only_xy"_a = false, //
            "round_z"_a = std::nullopt)
        .def(
            "load",
            [](mapbox::geojson::feature &self,
               const std::string &path) -> mapbox::geojson::feature & {
                if (endswith(path, ".pbf")) {
                    auto bytes = mapbox::geobuf::load_bytes(path);
                    auto geojson = mapbox::geobuf::Decoder().decode(bytes);
                    self = std::move(geojson.get<mapbox::geojson::feature>());
                    return self;
                }
                auto json = load_json(path);
                self = mapbox::geojson::convert<mapbox::geojson::feature>(json);
                return self;
            },
            rvp::reference_internal)
        .def(
            "dump",
            [](const mapbox::geojson::feature &self, //
               const std::string &path,              //
               bool indent,                          //
               bool sort_keys,                       //
               int precision,                        //
               bool only_xy) {
                if (endswith(path, ".pbf")) {
                    auto bytes = mapbox::geobuf::Encoder(
                                     std::pow(10, precision), only_xy)
                                     .encode(self);
                    return mapbox::geobuf::dump_bytes(path, bytes);
                }
                RapidjsonAllocator allocator;
                auto json = mapbox::geojson::convert(self, allocator);
                sort_keys_inplace(json);
                return dump_json(path, json, indent);
            },
            "path"_a, py::kw_only(), //
            "indent"_a = false,      //
            "sort_keys"_a = false,   //
            "precision"_a = 8,       //
            "only_xy"_a = false)
        //
        copy_deepcopy_clone(mapbox::geojson::feature)
        //
        .def(
            "round",
            [](mapbox::geojson::feature &self, int lon, int lat,
               int alt) -> mapbox::geojson::feature & {
                round_coords(self.geometry, lon, lat, alt);
                return self;
            },
            py::kw_only(), "lon"_a = 8, "lat"_a = 8, "alt"_a = 3,
            rvp::reference_internal) //
        GEOMETRY_DEDUPLICATE_XYZ(feature)
        //
        ;

    py::bind_vector<std::vector<mapbox::geojson::feature>>(
        geojson, "FeatureList", py::module_local())
        //
        .def("__call__", [](const std::vector<mapbox::geojson::feature> &self) {
            return to_python(self);
        });
    auto fc_binding = py::class_<mapbox::geojson::feature_collection,
                                 std::vector<mapbox::geojson::feature>>(
        geojson, "FeatureCollection", py::module_local());
    fc_binding.def(py::init<>())
        .def(py::init(
            [](const mapbox::geojson::feature_collection &g) { return g; }))
        .def(py::init([](int N) {
                 mapbox::geojson::feature_collection fc;
                 fc.resize(N);
                 return fc;
             }),
             "N"_a)
        .def(
            "resize",
            [](mapbox::geojson::feature_collection &self,
               int N) -> mapbox::geojson::feature_collection & {
                self.resize(N);
                return self;
            },
            rvp::reference_internal)
        //
        .def("__call__",
             [](const mapbox::geojson::feature_collection &self) {
                 return to_python(self);
             }) //
        .def(
            "round",
            [](mapbox::geojson::feature_collection &self, int lon, int lat,
               int alt) -> mapbox::geojson::feature_collection & {
                for (auto &f : self) {
                    round_coords(f.geometry, lon, lat, alt);
                }
                return self;
            },
            py::kw_only(), "lon"_a = 8, "lat"_a = 8, "alt"_a = 3,
            rvp::reference_internal)
            GEOMETRY_DEDUPLICATE_XYZ(feature_collection)
        // round
        //
        .def(
            "from_rapidjson",
            [](mapbox::geojson::feature_collection &self,
               const RapidjsonValue &json)
                -> mapbox::geojson::feature_collection & {
                self =
                    std::move(mapbox::geojson::convert(json)
                                  .get<mapbox::geojson::feature_collection>());
                return self;
            },
            rvp::reference_internal)
        .def("to_rapidjson",
             [](const mapbox::geojson::feature_collection &self) {
                 RapidjsonAllocator allocator;
                 auto json = mapbox::geojson::convert(self, allocator);
                 return json;
             })
        //
        .def(
            "from_geobuf",
            [](mapbox::geojson::feature_collection &self,
               const std::string &bytes)
                -> mapbox::geojson::feature_collection & {
                auto geojson = mapbox::geobuf::Decoder().decode(bytes);
                self = std::move(
                    geojson.get<mapbox::geojson::feature_collection>());
                return self;
            },
            rvp::reference_internal)
        .def(
            "to_geobuf",
            [](const mapbox::geojson::feature_collection &self, //
               int precision, bool only_xy, std::optional<int> round_z) {
                auto bytes = mapbox::geobuf::Encoder(std::pow(10, precision),
                                                     only_xy, round_z)
                                 .encode(self);
                return py::bytes(bytes);
            },
            py::kw_only(),       //
            "precision"_a = 8,   //
            "only_xy"_a = false, //
            "round_z"_a = std::nullopt)
        .def(
            "load",
            [](mapbox::geojson::feature_collection &self,
               const std::string &path)
                -> mapbox::geojson::feature_collection & {
                if (endswith(path, ".pbf")) {
                    auto bytes = mapbox::geobuf::load_bytes(path);
                    auto geojson = mapbox::geobuf::Decoder().decode(bytes);
                    self = std::move(
                        geojson.get<mapbox::geojson::feature_collection>());
                    return self;
                }
                auto json = load_json(path);
                self =
                    std::move(mapbox::geojson::convert(json)
                                  .get<mapbox::geojson::feature_collection>());
                return self;
            },
            rvp::reference_internal)
        .def(
            "dump",
            [](const mapbox::geojson::feature_collection &self,
               const std::string &path, //
               bool indent,             //
               bool sort_keys,          //
               int precision,           //
               bool only_xy) {
                if (endswith(path, ".pbf")) {
                    auto bytes = mapbox::geobuf::Encoder(
                                     std::pow(10, precision), only_xy)
                                     .encode(self);
                    return mapbox::geobuf::dump_bytes(path, bytes);
                }
                RapidjsonAllocator allocator;
                auto json = mapbox::geojson::convert(self, allocator);
                sort_keys_inplace(json);
                return dump_json(path, json, indent);
            },
            "path"_a, py::kw_only(), //
            "indent"_a = false,      //
            "sort_keys"_a = false,   //
            "precision"_a = 8,       //
            "only_xy"_a = false)
        //
        copy_deepcopy_clone(mapbox::geojson::feature_collection)
        //
        BIND_PY_FLUENT_ATTRIBUTE(mapbox::geojson::feature_collection, //
                                 PropertyMap,                         //
                                 custom_properties)                   //
        .def(
            "keys",
            [](mapbox::geojson::feature_collection &self) {
                return py::make_key_iterator(self.custom_properties);
            },
            py::keep_alive<0, 1>())
        .def(
            "values",
            [](mapbox::geojson::feature_collection &self) {
                return py::make_value_iterator(self.custom_properties);
            },
            py::keep_alive<0, 1>())
        .def(
            "items",
            [](mapbox::geojson::feature_collection &self) {
                return py::make_iterator(self.custom_properties);
            },
            py::keep_alive<0, 1>())
        .def(
            "__getitem__",
            [](mapbox::geojson::feature_collection &self,
               const std::string &key) -> mapbox::geojson::value * {
                // don't try "type", "features"
                auto &props = self.custom_properties;
                auto itr = props.find(key);
                if (itr == props.end()) {
                    return nullptr;
                }
                return &itr->second;
            },
            rvp::reference_internal)
        .def("__setitem__",
             [](mapbox::geojson::feature_collection &self,
                const std::string &key, const py::object &value) {
                 if (key == "type" || key == "features") {
                     throw pybind11::key_error(key);
                 }
                 self.custom_properties[key] = to_geojson_value(value);
                 return value;
             })
        .def("__delitem__", [](mapbox::geojson::feature_collection &self,
                               const std::string &key) {
            return self.custom_properties.erase(key);
        });
    //
    ;

    // copied from stl_bind.h
    using Vector = mapbox::geojson::feature_collection;
    using T = typename Vector::value_type;
    using SizeType = typename Vector::size_type;
    using DiffType = typename Vector::difference_type;

    auto wrap_i = [](DiffType i, SizeType n) {
        if (i < 0) {
            i += n;
        }
        if (i < 0 || (SizeType)i >= n) {
            throw py::index_error();
        }
        return i;
    };

    auto cl = fc_binding;
    cl.def(
        "__getitem__",
        [wrap_i](Vector &v, DiffType i) -> T & {
            i = wrap_i(i, v.size());
            return v[(SizeType)i];
        },
        rvp::reference_internal); // ref + keepalive
    cl.def("__setitem__", [wrap_i](Vector &v, DiffType i, const T &t) {
        i = wrap_i(i, v.size());
        v[(SizeType)i] = t;
    });
    cl.def(
        "__getitem__",
        [](const Vector &v, const py::slice &slice) -> Vector * {
            size_t start = 0, stop = 0, step = 0, slicelength = 0;

            if (!slice.compute(v.size(), &start, &stop, &step, &slicelength)) {
                throw py::error_already_set();
            }

            auto *seq = new Vector();
            seq->reserve((size_t)slicelength);

            for (size_t i = 0; i < slicelength; ++i) {
                seq->push_back(v[start]);
                start += step;
            }
            return seq;
        },
        py::arg("s"), "Retrieve list elements using a slice object");

    fc_binding.def(
        "__setitem__",
        [](Vector &v, const py::slice &slice, const Vector &value) {
            size_t start = 0, stop = 0, step = 0, slicelength = 0;
            if (!slice.compute(v.size(), &start, &stop, &step, &slicelength)) {
                throw py::error_already_set();
            }

            if (slicelength != value.size()) {
                throw std::runtime_error("Left and right hand size of slice "
                                         "assignment have different sizes!");
            }

            for (size_t i = 0; i < slicelength; ++i) {
                v[start] = value[i];
                start += step;
            }
        },
        "Assign list elements using a slice object");

    cl.def(
        "__delitem__",
        [wrap_i](Vector &v, DiffType i) {
            i = wrap_i(i, v.size());
            v.erase(v.begin() + i);
        },
        "Delete the list elements at index ``i``");

    cl.def(
        "__delitem__",
        [](Vector &v, const py::slice &slice) {
            size_t start = 0, stop = 0, step = 0, slicelength = 0;

            if (!slice.compute(v.size(), &start, &stop, &step, &slicelength)) {
                throw py::error_already_set();
            }

            if (step == 1 && false) {
                v.erase(v.begin() + (DiffType)start,
                        v.begin() + DiffType(start + slicelength));
            } else {
                for (size_t i = 0; i < slicelength; ++i) {
                    v.erase(v.begin() + DiffType(start));
                    start += step - 1;
                }
            }
        },
        "Delete list elements using a slice object");
}
} // namespace cubao
