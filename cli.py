import click
from pathlib import Path
import aiohttp
import asyncio
from functools import update_wrapper

def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))
    return update_wrapper(wrapper, f)


ALLOWED_EXTENSIONS = set(['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif'])


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("files", type=click.Path(exists=True, resolve_path=True), nargs=-1)
@coro
async def cli(files):

    # generate a list of absolute paths containing the files to be compared
    sequences = [Path(sequence) for sequence in files]
    files = [path for path in sequences if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS]

    # get all the files in the passed directories
    for directory in [path for path in sequences if path.is_dir()]:
        for f in directory.iterdir():
            if f.suffix.lower() in ALLOWED_EXTENSIONS:
                files.append(f)
    files = sorted(list(set(files)), key=lambda x: str(x.absolute())) # remove any duplicates and sort for cleaner log output

    print(files)

    async with aiohttp.ClientSession() as session:
        f = {'file': open(files[0], 'rb')}
        async with session.post("https://v6ukxwg624.execute-api.us-east-1.amazonaws.com/dev", data=f) as resp:
            print(await resp.text())
    #
    # #compute compressed sizes of individual sequences
    # click.secho("Compressing individual files...", fg="green")
    # compressed_sizes = tqdm_parallel_map(executor,
    #                                      lambda x: compressed_size(
    #                                          sequences=x,
    #                                          algorithm=compression,
    #                                          save_directory=saveCompression,
    #                                          reverse_complement=reverse_complement,
    #                                          BWT=BWT,
    #                                          bwte_inputs=bwte_inputs),
    #                                      showProgress,
    #                                      files)
    # compressed_dict = dict(compressed_sizes) # {PATH: compressed size}
    #
    # # compute compressed sizes of all ordered pairs of sequences
    # click.secho("Compressing pairs...", fg="green")
    # compressed_pairs_sizes = tqdm_parallel_map(executor,
    #                                            lambda x: compressed_size(
    #                                                sequences=x,
    #                                                algorithm=compression,
    #                                                save_directory=saveCompression,
    #                                                reverse_complement=reverse_complement,
    #                                                BWT=BWT,
    #                                                bwte_inputs=bwte_inputs),
    #                                            showProgress,
    #                                            itertools.product(compressed_dict.keys(), repeat=2))
    #
    # compressed_pairs_dict = dict(compressed_pairs_sizes) # {(A, B): size, (B, A): size,...}
    #
    # distances = {}
    # for pair in itertools.product(compressed_dict.keys(), repeat=2):
    #     distances[pair] = compute_distance(compressed_dict[pair[0]],
    #                                        compressed_dict[pair[1]],
    #                                        compressed_pairs_dict[(pair[0], pair[1])],
    #                                        compressed_pairs_dict[(pair[1], pair[0])])
    #
    # distances = list(distances.items())
    # distances = [(distance[0][0], distance[0][1], distance[1]) for distance in distances]
    # df = pd.DataFrame(distances, columns=["file", "file2", "ncd"])#.to_csv("out.csv", index=False)
    # df = df.pivot(index='file', columns='file2', values='ncd')
    # df.to_csv(output)
    # df = pd.read_csv(output)
    # df.columns = list(map(lambda x: Path(x).name, df.columns))
    # df.file = df.file.apply(lambda x: Path(x).name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(cli())
finally:
    loop.close()
