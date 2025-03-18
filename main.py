import docker
import time

# Initialize Docker client
client = docker.from_env()

def create_sandbox():
    """
    Create a Docker container as a sandbox environment.
    """
    print("Creating sandbox environment...")
    try:
        container = client.containers.run(
            image="ubuntu-ping",  # Use the custom image
            command="ping -c 5 google.com",  # Run ping directly
            detach=True,  # Run in the background
            tty=True,  # Allocate a pseudo-TTY
            network_disabled=False,  # Enable network access
            dns=["8.8.8.8", "8.8.4.4"],  # Use Google DNS
            read_only=False,  # Allow writing to the filesystem
            user="root",  # Run as root
        )
        print(f"Sandbox container created with ID: {container.id}")
        return container
    except Exception as e:
        print(f"Error creating sandbox: {e}")
        return None

def monitor_sandbox(container):
    """
    Monitor the sandbox container for activity.
    """
    print("Monitoring sandbox...")
    try:
        logs = container.logs(stream=True)
        buffer = ""  # Buffer to accumulate log data
        for chunk in logs:
            # Decode the chunk and add it to the buffer
            buffer += chunk.decode("utf-8")
            # Split the buffer into lines
            lines = buffer.split("\n")
            # Print all lines except the last one (which may be incomplete)
            for line in lines[:-1]:
                print(line.strip())
            # Keep the last (possibly incomplete) line in the buffer
            buffer = lines[-1]
    except Exception as e:
        print(f"Error monitoring sandbox: {e}")

def stop_sandbox(container):
    """
    Stop and remove the sandbox container.
    """
    print("Stopping sandbox...")
    try:
        container.stop()
        container.remove()
        print("Sandbox stopped and removed.")
    except Exception as e:
        print(f"Error stopping sandbox: {e}")

def main():
    # Create the sandbox
    container = create_sandbox()
    if not container:
        return

    # Monitor the sandbox for a few seconds
    try:
        monitor_sandbox(container)
        time.sleep(10)  # Monitor for 10 seconds
    except KeyboardInterrupt:
        print("Stopping monitoring...")

    # Stop the sandbox
    stop_sandbox(container)

if __name__ == "__main__":
    main()
