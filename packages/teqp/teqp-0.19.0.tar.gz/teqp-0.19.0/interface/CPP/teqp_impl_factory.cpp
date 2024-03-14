#include "teqp/cpp/teqpcpp.hpp"
#include "teqp/models/fwd.hpp"
#include "teqp/cpp/deriv_adapter.hpp"

// This large block of schema definitions is populated by cmake
// at cmake configuration time
extern const nlohmann::json model_schema_library;

namespace teqp {
    namespace cppinterface {

        std::unique_ptr<teqp::cppinterface::AbstractModel> make_SAFTVRMie(const nlohmann::json &j);

        using makefunc = ModelPointerFactoryFunction;
        using namespace teqp::cppinterface::adapter;
    
        nlohmann::json get_model_schema(const std::string& kind) { return model_schema_library.at(kind); }

        // A list of factory functions that maps from EOS kind to factory function
        // The factory function returns a pointer to an AbstractModel (but which is an instance of a derived class)
        static std::unordered_map<std::string, makefunc> pointer_factory = {
            {"vdW1", [](const nlohmann::json& spec){ return make_owned(vdWEOS1(spec.at("a"), spec.at("b"))); }},
            {"vdW", [](const nlohmann::json& spec){ return make_owned(vdWEOS<double>(spec.at("Tcrit / K"), spec.at("pcrit / Pa"))); }},
            {"PR", [](const nlohmann::json& spec){ return make_owned(make_canonicalPR(spec));}},
            {"SRK", [](const nlohmann::json& spec){ return make_owned(make_canonicalSRK(spec));}},
            {"cubic", [](const nlohmann::json& spec){ return make_owned(make_generalizedcubic(spec));}},
            {"QCPRAasen", [](const nlohmann::json& spec){ return make_owned(QuantumCorrectedPR(spec));}},
            {"advancedPRaEres", [](const nlohmann::json& spec){ return make_owned(make_AdvancedPRaEres(spec));}},
            {"RKPRCismondi2005", [](const nlohmann::json& spec){ return make_owned(RKPRCismondi2005(spec));}},
            
            {"CPA", [](const nlohmann::json& spec){ return make_owned(CPA::CPAfactory(spec));}},
            {"PCSAFT", [](const nlohmann::json& spec){ return make_owned(PCSAFT::PCSAFTfactory(spec));}},
            
            {"LKP", [](const nlohmann::json& spec){ return make_owned(LKP::make_LKPMix(spec));}},
            
            {"multifluid", [](const nlohmann::json& spec){ return make_owned(multifluidfactory(spec));}},
            {"multifluid-ECS-HuberEly1994", [](const nlohmann::json& spec){ return make_owned(ECSHuberEly::ECSHuberEly1994(spec));}},
            {"SW_EspindolaHeredia2009",  [](const nlohmann::json& spec){ return make_owned(squarewell::EspindolaHeredia2009(spec.at("lambda")));}},
            {"EXP6_Kataoka1992", [](const nlohmann::json& spec){ return make_owned(exp6::Kataoka1992(spec.at("alpha")));}},
            {"AmmoniaWaterTillnerRoth", [](const nlohmann::json& /*spec*/){ return make_owned(AmmoniaWaterTillnerRoth());}},
            {"LJ126_TholJPCRD2016", [](const nlohmann::json& /*spec*/){ return make_owned(build_LJ126_TholJPCRD2016());}},
            {"LJ126_KolafaNezbeda1994", [](const nlohmann::json& /*spec*/){ return make_owned(LJ126KolafaNezbeda1994());}},
            {"LJ126_Johnson1993", [](const nlohmann::json& /*spec*/){ return make_owned(LJ126Johnson1993());}},
            {"Mie_Pohl2023", [](const nlohmann::json& spec){ return make_owned(Mie::Mie6Pohl2023(spec.at("lambda_a")));}},
            {"2CLJF-Dipole", [](const nlohmann::json& spec){ return make_owned(twocenterljf::build_two_center_model_dipole(spec.at("author"), spec.at("L^*"), spec.at("(mu^*)^2")));}},
            {"2CLJF-Quadrupole", [](const nlohmann::json& spec){ return make_owned(twocenterljf::build_two_center_model_quadrupole(spec.at("author"), spec.at("L^*"), spec.at("(Q^*)^2")));}},
            {"IdealHelmholtz", [](const nlohmann::json& spec){ return make_owned(IdealHelmholtz(spec));}},
            
            {"GERG2004resid", [](const nlohmann::json& spec){ return make_owned(GERG2004::GERG2004ResidualModel(spec.at("names")));}},
            {"GERG2008resid", [](const nlohmann::json& spec){ return make_owned(GERG2008::GERG2008ResidualModel(spec.at("names")));}},
            {"GERG2004idealgas", [](const nlohmann::json& spec){ return make_owned(GERG2004::GERG2004IdealGasModel(spec.at("names")));}},
            {"GERG2008idealgas", [](const nlohmann::json& spec){ return make_owned(GERG2008::GERG2008IdealGasModel(spec.at("names")));}},
            
            // Implemented in its own compilation unit to help with compilation time
            {"SAFT-VR-Mie", [](const nlohmann::json& spec){ return make_SAFTVRMie(spec); }}
        };

        std::unique_ptr<teqp::cppinterface::AbstractModel> build_model_ptr(const nlohmann::json& json, const bool validate) {
            
            // Extract the name of the model and the model parameters
            std::string kind = json.at("kind");
            auto spec = json.at("model");
            
            // Read in flag to enable/disable validation, if present
            bool validate_in_json = json.value("validate", true);
            
            auto itr = pointer_factory.find(kind);
            if (itr != pointer_factory.end()){
                if (validate || validate_in_json){
                    if (model_schema_library.contains(kind)){
                        // This block is not thread-safe, needs a mutex or something
                        JSONValidator validator(model_schema_library.at(kind));
                        if (!validator.is_valid(spec)){
                            throw teqp::JSONValidationError(validator.get_validation_errors(spec));
                        }
                    }
                }
                return (itr->second)(spec);
            }
            else{
                throw std::invalid_argument("Don't understand \"kind\" of: " + kind);
            }
        }
    
        std::unique_ptr<AbstractModel> make_multifluid_model(const std::vector<std::string>& components, const std::string& coolprop_root, const std::string& BIPcollectionpath, const nlohmann::json& flags, const std::string& departurepath) {
            return make_owned(build_multifluid_model(components, coolprop_root, BIPcollectionpath, flags, departurepath));
        }
    
        std::unique_ptr<AbstractModel> make_model(const nlohmann::json& j, const bool validate) {
            return build_model_ptr(j, validate);
        }
    
        void add_model_pointer_factory_function(const std::string& key, ModelPointerFactoryFunction& func){
            if (pointer_factory.find(key) == pointer_factory.end()){
                pointer_factory[key] = func;
            }
            else{
                throw teqp::InvalidArgument("key is already present, overwriting is not currently allowed");
            }
        }
    }
}
