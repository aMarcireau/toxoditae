import  krpc
import time
import json

################################## Parameters #########################################

Kp_speed = 0.15 # varies from rocket type, tweek this parameter to fit your rocket type
vertical_speed_target=30 # 30m/s is a correct value to get correct datas
altitude_target = 80000 # 80 000m allows to get data for all the atmosphere of Kerbin
file_name = "flight_log.json"

#######################################################################################

conn = krpc.connect(name='Weather probe')
vessel=conn.space_center.active_vessel
vessel.auto_pilot.target_pitch_and_heading(90,90)
vessel.auto_pilot.engage()
vessel.control.throttle = 1
time.sleep(1)
samples = []

vessel.control.activate_next_stage()

while vessel.flight().mean_altitude<= altitude_target :
    # While rocket altitude is above
    samples.append({'g_force' : vessel.flight().g_force,
    'mean_altitude' : vessel.flight().mean_altitude,
    'surface_altitude' : vessel.flight().surface_altitude,
    'bedrock_altitude' : vessel.flight().bedrock_altitude,
    'elevation' : vessel.flight().elevation,
    'latitude' : vessel.flight().latitude,
    'longitude' : vessel.flight().longitude,
    'velocity' : vessel.flight().velocity,
    'speed' : vessel.flight().speed,
    'horizontal_speed' : vessel.flight().horizontal_speed,
    'vertical_speed' : vessel.flight().vertical_speed,
    'center_of_mass' : vessel.flight().center_of_mass,
    'rotation' : vessel.flight().rotation,
    'direction' : vessel.flight().direction,
    'pitch' : vessel.flight().pitch,
    'heading' : vessel.flight().heading,
    'roll' : vessel.flight().roll,
    'prograde' : vessel.flight().prograde,
    'retrograde': vessel.flight().retrograde,
    'normal': vessel.flight().normal,
    'anti_normal': vessel.flight().anti_normal,
    'radial': vessel.flight().radial,
    'anti_radial': vessel.flight().anti_radial,
    'atmosphere_density': vessel.flight().atmosphere_density,
    'dynamic_pressure': vessel.flight().dynamic_pressure,
    'static_pressure': vessel.flight().static_pressure,
    'static_pressure_at_msl': vessel.flight().static_pressure_at_msl,
    'aerodynamic_force': vessel.flight().aerodynamic_force,
    'lift': vessel.flight().lift,
    'drag': vessel.flight().drag,
    'speed_of_sound': vessel.flight().speed_of_sound,
    'mach': vessel.flight().mach,
    'true_air_speed': vessel.flight().true_air_speed,
    'equivalent_air_speed': vessel.flight().equivalent_air_speed,
    'terminal_velocity': vessel.flight().terminal_velocity,
    'angle_of_attack': vessel.flight().angle_of_attack,
    'sideslip_angle': vessel.flight().sideslip_angle,
    'total_air_temperature': vessel.flight().total_air_temperature,
    'static_air_temperature': vessel.flight().static_air_temperature})

    vertical_speed_error=vertical_speed_target-vessel.flight(vessel.orbit.body.reference_frame).vertical_speed
    if vessel.control.throttle+Kp_speed*vertical_speed_error>1:
        vessel.control.throttle=1
    elif vessel.control.throttle+Kp_speed*vertical_speed_error<0:
        vessel.control.throttle=0
    else:
        vessel.control.throttle+=Kp_speed*vertical_speed_error
        
with open(file_name,'w') as file:
    json.dump(samples,file)
