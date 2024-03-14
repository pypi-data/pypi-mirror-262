#include <catch2/catch_test_macros.hpp>
#include <catch2/benchmark/catch_benchmark_all.hpp>

#include "teqp/cpp/teqpcpp.hpp"
#include "teqp/cpp/derivs.hpp"
#include "teqp/derivs.hpp"
#include "teqp/cpp/deriv_adapter.hpp"
#include "teqp/models/multifluid.hpp"
#include "teqp/models/GERG/GERG.hpp"

using namespace teqp;

TEST_CASE("GERG2008 parts", "[GERG2008]")
{
    BENCHMARK("bg"){
        return GERG2008::get_betasgammas("methane","n-decane");
    };
    BENCHMARK("bg backwards"){
        return GERG2008::get_betasgammas("n-decane", "methane");
    };
    BENCHMARK("bg fallback to 2004"){
        return GERG2008::get_betasgammas("ethane", "methane");
    };
}

TEST_CASE("multifluid derivatives", "[mf]")
{
    nlohmann::json j = {
        {"kind", "multifluid"},
        {"model", {
            {"components", {"../mycp/dev/fluids/Methane.json"}},
            {"BIP", "../mycp/dev/mixtures/mixture_binary_pairs.json"},
            {"departure", "../mycp/dev/mixtures/mixture_departure_functions.json"}
        }
    }};
    //std::cout << j.dump(2);
    auto am = teqp::cppinterface::make_model(j);

    auto z = (Eigen::ArrayXd(1) << 1.0).finished();
    auto rhovec = 300.0* z;
    
    BENCHMARK("construction"){
        return teqp::cppinterface::make_model(j);
    };
    BENCHMARK("alphar") {
        return am->get_Arxy(0, 0, 300, 3.0, z);
    };
    BENCHMARK("Ar20") {
        return am->get_Ar20(300, 3.0, z);
    };
    BENCHMARK("get_Ar02n") {
        return am->get_Ar02n(300, 3.0, z);
    };
    BENCHMARK("fugacity coefficients") {
        return am->get_fugacity_coefficients(300.0, rhovec);
    };
    BENCHMARK("cvr/R") {
        return -1*am->get_Arxy(2, 0, 300, 3.0, z);
    };
    BENCHMARK("partial_molar_volumes") {
        return am->get_partial_molar_volumes(300.0, rhovec);
    };
    BENCHMARK("get_deriv_mat2") {
        return am->get_deriv_mat2(300.0, 3.0, z);
    };
    BENCHMARK("build_iteration_Jv") {
        auto mat = am->get_deriv_mat2(300.0, 3.0, z);
        auto mat2 = am->get_deriv_mat2(300.0, 3.0, z);
        const std::vector<char> vars = {'T','D','P','S'};
        return teqp::cppinterface::build_iteration_Jv(vars, mat, mat2, 8.3144, 300.0, 300.0, z);
    };
}

TEST_CASE("multifluid derivatives via DerivativeAdapter", "[mf]")
{
    nlohmann::json j = {
        {"kind", "multifluid"},
        {"model", {
            {"components", {"../mycp/dev/fluids/Methane.json"}},
            {"BIP", "../mycp/dev/mixtures/mixture_binary_pairs.json"},
            {"departure", "../mycp/dev/mixtures/mixture_departure_functions.json"}
        }
    }};
    const auto am = teqp::cppinterface::make_model(j);
    using multifluid_t = decltype(multifluidfactory(nlohmann::json{}));
    auto model = teqp::cppinterface::adapter::get_model_cref<multifluid_t>(am.get());

    auto z = (Eigen::ArrayXd(1) << 1.0).finished();
    
    using namespace cppinterface;
    using vd = VirialDerivatives<decltype(model), double, decltype(z)>;
    
    BENCHMARK("B4 natively") {
        return vd::get_Bnvir<4>(model, 300.0, z);
    };
    BENCHMARK("B4 via AbstractModel") {
        return am->get_Bnvir(4, 300, z);
    };
    BENCHMARK("B4 via DerivativeAdapter") {
        using namespace teqp::cppinterface::adapter;
        return view(model)->get_Bnvir(4, 300, z);
    };
}


TEST_CASE("GERG2008 derivatives", "[GERG2008]")
{
    nlohmann::json j = {
        {"kind", "GERG2008resid"},
        {"model", {
            {"names", {"methane","ethane","propane","n-butane"}},
        }
    }};
    //std::cout << j.dump(2);
    

    auto z = (Eigen::ArrayXd(1) << 1.0).finished();
    auto rhovec = 300.0* z;
    auto am = teqp::cppinterface::make_model(j);
    
    BENCHMARK("construction"){
        return teqp::cppinterface::make_model(j);
    };
    BENCHMARK("alphar") {
        return am->get_Arxy(0, 0, 300, 3.0, z);
    };
    BENCHMARK("Ar20") {
        return am->get_Ar20(300, 3.0, z);
    };
    BENCHMARK("get_Ar02n") {
        return am->get_Ar02n(300, 3.0, z);
    };
    BENCHMARK("fugacity coefficients") {
        return am->get_fugacity_coefficients(300.0, rhovec);
    };
    BENCHMARK("cvr/R") {
        return -1*am->get_Arxy(2, 0, 300, 3.0, z);
    };
    BENCHMARK("partial_molar_volumes") {
        return am->get_partial_molar_volumes(300.0, rhovec);
    };
    BENCHMARK("get_deriv_mat2") {
        return am->get_deriv_mat2(300.0, 3.0, z);
    };
    BENCHMARK("build_iteration_Jv") {
        auto mat = am->get_deriv_mat2(300.0, 3.0, z);
        auto mat2 = am->get_deriv_mat2(300.0, 3.0, z);
        const std::vector<char> vars = {'T','D','P','S'};
        return teqp::cppinterface::build_iteration_Jv(vars, mat, mat2, 8.3144, 300.0, 300.0, z);
    };
}
