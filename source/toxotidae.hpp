#pragma once

#include <cmath>
#include <cstdint>
#include <stdexcept>
#include <vector>

/// toxotidae is a KSP rocket simulator.
namespace toxotidae {
    /// properties lists a stage's static properties.
    struct properties {
        float empty_mass;
        float propellant_mass;
    };

    /// state stores the simulation variables.
    struct state {
        std::size_t stage;
        float t;
        float x;
        float y;
        float vx;
        float vy;
        float theta;
        float dtheta;
        float mass;
    };

    /// control sets the throttle and wether the simulation must keep going.
    /// staging is handle by the simulator.
    struct control {
        float d2theta;
        float throttle;
        bool is_running;
    };

    /// simulate runs a step-by-step simulation.
    ///     isp(std::size_t stage, float rho) -> float
    ///     drag(std::size_t stage, float rho, float air_speed, float air_angle) -> float
    ///     thrust(std::size_t stage, float rho) -> float
    ///     state_to_control(state current_state) -> control
    template <typename Isp, typename Drag, typename Thrust, typename StateToControl>
    inline state simulate(
        std::vector<properties> stage_to_properties,
        Isp isp,
        Drag drag,
        Thrust thrust,
        StateToControl state_to_control) {
        if (stage_to_properties.empty()) {
            throw std::logic_error("there must be at least one stage");
        }

        // constants
        const float G = 6.67408e-11;
        const float delta_t = 0.02f;
        const float omega = 2 * M_PI / 21549.425;
        const float kerbin_radius = 600000;
        const float kerbin_mass = 5.2915158e22;

        // state variables
        auto current_properties = stage_to_properties[0];
        state current_state{0,                                                                   // stage
                            0,                                                                   // t
                            0,                                                                   // x
                            kerbin_radius,                                                       // y
                            kerbin_radius * omega,                                               // vx
                            0,                                                                   // vy
                            M_PI_2,                                                              // theta,
                            0,                                                                   // dtheta
                            current_properties.empty_mass + current_properties.propellant_mass}; // mass

        // run the simulation
        for (;;) {
            const control current_control = state_to_control(current_state);
            if (!current_control.is_running) {
                break;
            }

            // pre-calculations
            const auto r = std::hypot(current_state.x, current_state.y);
            const auto z = r - kerbin_radius;
            const auto rho = z < 70000 ? 1.223125f * 0.008f * std::exp(-z / 5000) : 0.0f;
            const auto air_vx = omega * current_state.y - current_state.vx;
            const auto air_vy = -omega * current_state.x - current_state.vy;
            const auto air_angle = std::atan2(air_vx, air_vy);

            // callbacks
            const auto current_isp = isp(current_state.stage, rho);
            const auto current_drag =
                drag(current_state.stage, rho, std::hypot(air_vx, air_vy), air_angle - current_state.theta);
            const auto current_thrust = thrust(current_state.stage, rho);

            // discrete derivative
            current_state = state{
                current_state.stage,
                current_state.t + delta_t,
                current_state.x + current_state.vx * delta_t,
                current_state.y + current_state.vy * delta_t,
                current_state.vx
                    + (current_control.throttle * current_thrust / current_state.mass * std::cos(current_state.theta)
                       - G * kerbin_mass / std::pow(r, 3.0f) * current_state.x
                       - current_drag / current_state.mass * std::cos(air_angle))
                          * delta_t,
                current_state.vy
                    + (current_control.throttle * current_thrust / current_state.mass * std::sin(current_state.theta)
                       - G * kerbin_mass / std::pow(r, 3.0f) * current_state.y
                       - current_drag / current_state.mass * std::sin(air_angle))
                          * delta_t,
                current_state.theta + current_state.dtheta * delta_t,
                current_state.dtheta + current_control.d2theta * delta_t,
                current_state.mass - current_thrust / current_isp * delta_t};

            // staging
            if (current_state.mass <= current_properties.empty_mass) {
                ++current_state.stage;
                if (current_state.stage >= stage_to_properties.size()) {
                    break;
                }
                current_properties = stage_to_properties[current_state.stage];
            }
        }
        return current_state;
    }
}
