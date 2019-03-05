#include "../source/toxotidae.hpp"
#include <iomanip>
#include <iostream>

int main(int argc, char* argv[]) {
    for (const auto name : {"t", "x", "y", "vx", "vy", "theta", "dtheta", "mass"}) {
        std::cout << std::setw(15) << name;
    }
    std::cout << std::endl;
    const auto final_state = toxotidae::simulate(
        {{100, 1000}},
        [](std::size_t stage, float rho) -> float { return 1000; },
        [](std::size_t stage, float rho, float air_speed, float air_angle) -> float { return 0; },
        [](std::size_t stage, float rho) -> float { return 20000; },
        [](toxotidae::state state) -> toxotidae::control {
            for (const auto value :
                 {state.t, state.x, state.y, state.vx, state.vy, state.theta, state.dtheta, state.mass}) {
                std::cout << std::setw(15) << value;
            }
            std::cout << std::endl;
            return {0, 1, true};
        });
    return 0;
}
