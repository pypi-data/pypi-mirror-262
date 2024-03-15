import os
import typing
from sprinko.core.ctx import SprinkoCtx
from sprinko.core.ko import Ko
from sprinko.utils import SingletonMeta
from masscodeDriver import Snippet, Tag
from masscodeDriver.utils import FuzzyContext

class Sprinko(metaclass=SingletonMeta):
    def __init__(self, check : typing.Union[str, bool] = None, reset : bool = False):
        if check is None:
            self.__ko = None
        elif isinstance(check, bool):
            self.__ko = Ko()
        
        elif reset and isinstance(check, str):
            Ko.reset()
            self.__ko = Ko() 
            self.__ko.setup(check)
        elif isinstance(check, str):
            os.environ["SPRINKO_PASSWORD"] = check
            self.__ko = Ko()
        else:
            raise ValueError("invalid check value")

    
    def query(
        self, 
        query : str, 
        confidence : float = 0.7, 
        ignore_security : bool = False, 
        ignore_limit : bool = False,
        only_warn : bool = False
    ):
        if "[" in query and query.endswith("]"):
            i: int = query.index("[")
            indexquery = query[i + 1:]
            query = query[:i]
            if indexquery.isdigit():
                index = int(indexquery)
            else:
                index = indexquery
        else:
            index = 0

        if "::" in query:
            bottle, query = query.split("::")
            tagcond = f"sprinko:{bottle}"
        elif ignore_limit:
            tagcond = None
        else:
            tagcond = FuzzyContext("sprinko", justcontains=True)

        for snippet in Snippet.query(
            limit=-1, tag=Tag.query(name=tagcond), name=FuzzyContext(query, confidence=confidence)
        ):
            snippet : Snippet

            if isinstance(index, int):
                fs = snippet.content[index]["value"]
            else:
                # parse as x = y
                if "=" not in index:
                    x = "label"
                    y = index
                else:
                    x, y = index.split("=")
                    if x == "lang" or x == "l":
                        x = "language"

                for i, frag in enumerate(snippet.content):
                    if frag[x] == y:
                        fs = frag["value"]
                        break

            if ignore_security or ignore_limit or self.__ko is None:
                return fs
            
            if not self.__ko.check_id_hash(f"{snippet.id}[{index}]", fs):
                if only_warn:
                    input(f"Detected hash mismatch in {snippet.name} - {snippet.id}")
                else:
                    raise ValueError("invalid hash")
            
            return fs

        return None

    def run(
        self, *queries, confidence : float = 0.7, 
        ignore_security : bool = False, 
        ignore_limit : bool = False,
        only_warn : bool = False
    ):
        parsed = []
        for q in queries:
            if q.startswith("[") or q.startswith("{"):
                parsed.append(q)
            else:
                parsed.append(self.query(q, 
                                         confidence, 
                                         ignore_security, 
                                         ignore_limit,
                                         only_warn
                ))

        ctx = SprinkoCtx(*parsed)
        ctx.run()


    def meta(self):
        return self.__ko.meta()
        
    def generate(
        self,
    ):
        pass
    

    
    
