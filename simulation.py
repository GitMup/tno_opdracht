from patriot import Patriot

TIME_STEPS = 20

if __name__ == "__main__":
    patriot = Patriot()
    for i in range(TIME_STEPS):
        print(f"This is time step {i}")
        patriot.react(i)
        print("\n")