import os
import json
import time
from typing import List
from datetime import datetime
from autocoder.common import SourceCode, AutoCoderArgs

import pydantic
import byzerllm
import hashlib

class IndexItem(pydantic.BaseModel):
    module_name: str
    symbols: str
    last_modified: str
    md5: str  # 新增文件内容的MD5哈希值字段


class TargetFile(pydantic.BaseModel):
    file_path: str
    reason: str = pydantic.Field(...,description="The reason why the file is the target file") 

class FileList(pydantic.BaseModel):
    file_list: List[TargetFile]


class IndexManager:
    def __init__(self, llm, sources: List[SourceCode], args:AutoCoderArgs):
        self.sources = sources
        self.source_dir = args.source_dir
        self.anti_quota_limit = args.anti_quota_limit
        self.index_dir = os.path.join(self.source_dir, ".auto-coder")
        self.index_file = os.path.join(self.index_dir, "index.json")
        self.llm = llm

        # 如果索引目录不存在,则创建它
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)

    @byzerllm.prompt(lambda self: self.llm, render="jinja2")
    def _get_related_files(self,indices:str, file_paths: str) -> FileList:
        '''
        下面是所有文件以及对应的符号信息：
        
        {{ indices }}

        请参考上面的信息，找到被下列文件使用或者引用到的文件列表：
        
        {{ file_paths }}

        如果没有相关的文件，返回空即可
        '''
        

    @byzerllm.prompt(lambda self: self.llm, render="jinja2")
    def get_all_file_symbols(self, path: str, code: str) -> str:
        '''
        下列是文件 {{ path }} 的源码：
        
        {{ code }}
        
        从上述内容中获取文件中的符号。需要获取的符号类型包括：
        
        1. 函数
        2. 类  
        3. 变量
        4. 所有导入语句 
        
        如果没有任何符号,返回"没有任何符号"。
        最终结果按如下格式返回:

        符号类型: 符号名称, 符号名称, ...        
        '''

    def build_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as file:
                index_data = json.load(file)
        else:
            index_data = {}

        updated_sources = []

        for source in self.sources:
            file_path = source.module_name                                   
            md5 = hashlib.md5(source.source_code.encode('utf-8')).hexdigest()
            print(f"build index for {file_path} md5: {md5}")
            if source.source_code.strip() == "":
                continue

            if source.module_name in index_data and index_data[source.module_name]["md5"] == md5:
                continue
            
            try:
                symbols = self.get_all_file_symbols(source.module_name, source.source_code)
                time.sleep(self.anti_quota_limit)
            except Exception as e:
                print(f"Error: {e}")
                continue

            index_data[source.module_name] = {
                "symbols": symbols,
                "last_modified": os.path.getmtime(file_path),
                "md5": md5
            }
            updated_sources.append(source)

        if updated_sources:
            with open(self.index_file, "w") as file:
                json.dump(index_data, file, ensure_ascii=False, indent=2)

        return index_data

    def read_index(self) -> List[IndexItem]:
        if not os.path.exists(self.index_file):
            return []

        with open(self.index_file, "r") as file:
            index_data = json.load(file)

        index_items = []
        for module_name, data in index_data.items():
            index_item = IndexItem(
                module_name=module_name,
                symbols=data["symbols"],
                last_modified=data["last_modified"],
                md5=data["md5"]
            )
            index_items.append(index_item)

        return index_items

    def _get_meta_str(self):
        index_items = self.read_index()
        output = []
        for item in index_items:
            output.append(f"##{item.module_name}\n{item.symbols}\n\n")
        return "".join(output)  

    def get_related_files(self,file_paths:List[str]):
        return self._get_related_files(self._get_meta_str(),"\n".join(file_paths))
    
    @byzerllm.prompt(lambda self: self.llm, render="jinja2",print_prompt=True)
    def _get_target_files_by_query(self,indices:str,query:str)->FileList:
        '''
        下面是所有文件以及对应的符号信息：
        
        {{ indices }}

        请参考上面的信息，根据用户的问题寻找相关文件。如果没有相关的文件，返回空即可。

        用户的问题是：{{ query }}
        '''

    def get_target_files_by_query(self,query:str)->FileList:
        return self._get_target_files_by_query(self._get_meta_str(),query)  