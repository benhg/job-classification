if __name__ == "__main__":
    from parsl import *

    config = {
        "sites": [
            {
                "site": "GoogleCloudPlatform",
                "auth": {
                    "keyfile": "/Users/ben/Downloads/service_account_key.json",
                    "channel": None
                },
                "execution": {
                    "executor": "ipp",
                    "scriptDir": ".scripts",
                    "provider": "googlecloud",
                    "block": {
                        "nodes": 1,
                        "initBlocks": 1,
                        "minBlocks": 0,
                        "maxBlocks": 10,
                        "options": {
                            "projectID": "ace-matrix-193421",
                            "region": "us-west1",
                            "instanceType": "n1-standard-1",
                            "osProject": 'debian-cloud',
                            "osFamily": "debian-8",
                            "googleVersion": "v1",
                        }
                    }
                }
            }

        ],
        "globals": {"lazyErrors": True},
        "controller": {}
    }

    dfk = DataFlowKernel(config=config)

    @App('python', dfk)
    def pi(total):
        # App functions have to import modules they will use.
        import random
        # Set the size of the box (edge length) in which we drop random points
        edge_length = 10000
        center = edge_length / 2
        c2 = center ** 2
        count = 0

        for i in range(total):
            # Drop a random point in the box.
            x, y = random.randint(
                1, edge_length), random.randint(1, edge_length)
            # Count points within the circle
            if (x - center)**2 + (y - center)**2 < c2:
                count += 1

        return (count * 4 / total)

    @App('python', dfk)
    def avg_n(inputs=[]):
        return sum(inputs) / len(inputs)

    # Call the workflow:
    sims = [pi(10**6) for i in range(10)]
    avg_pi = avg_n([task.result() for task in sims])

    # Print the results
    print(("Average: {0:.63f}".format(avg_pi.result())))
