from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote
from seed import main as main_seed

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find tag by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags: str):
    # result = []
    tags = tags.split(',')
    quotes = Quote.objects(tags__in=tags)
    # for tag in tags:
    #     result.extend(find_by_tag(tag.strip()))
    return [quote.to_json() for quote in quotes]


@cache
def find_by_author(author: str) -> dict[Any, list]:
    print(f"Find author by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


commands = {'name': find_by_author, 'tag': find_by_tag, 'tags': find_by_tags}


def parser_command(value: str):
    if value == 'exit':
        return exit()
    try:
        command, args = value.split(':')
        return [command, args.strip()]
    except ValueError:
        return


def main():
    while True:
        command = parser_command(input('>>>'))
        # print(command)
        if command and command[0] in commands.keys() and command[1]:
            print(commands[command[0]](command[1]))
        else:
            print('Incorrect command')


if __name__ == '__main__':
    main_seed()
    main()
