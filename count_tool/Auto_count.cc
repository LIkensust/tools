#include <iostream>
#include <unistd.h>
#include <string>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include "checktool.h"
using namespace std;

int files = 0;

bool match(string name) {
  auto check_tool = RegexTool::make();
  check_tool->set_regex("(\\.cc$|\\.c$|\\.h$|\\.hpp$|\\.cxx$|\\.java$|\\.py$)");
  vector<pair<int,int>> ret = check_tool->check_str(name.c_str());
  check_tool.release();
  if(!ret.empty()) {
    return true;
  }
  return false;
}

int count_num(string& name) {
  FILE* fin = fopen(name.c_str(),"r");
  if(fin == NULL) return -1;
  int num = 0;
  while(!feof(fin)) {
    char c = fgetc(fin);
    if(c == '\n') num++;
  }
  fclose(fin);
  return num;
}

int open_and_read(string path,int &totle,bool flag,bool all) {
  if(path.empty()) return 0;
  DIR *dp;
  struct dirent* dirrp;
  struct stat buf;
  if(lstat(path.c_str(),&buf) == -1) {
    perror("lstat");
    _exit(1);
  } 
  if(!S_ISDIR(buf.st_mode)) {
    if(match(path)) {
      int num = count_num(path);
      if(num != -1) {
        files += 1;
        totle += num;
        if(flag) {
          cout<<"["<<path<<"]"<<" "<<"["<<num<<"]"<<endl;
        }
      }
    }
  } else {
    if(path[path.size()-1] != '/') path+='/';
    if(all)
      cout<<"<==into:==> "<<path<<endl;
    dp = opendir(path.c_str());
    if(dp == NULL) {cout<<"[==open file==]"<<endl;return 0;}
    while((dirrp = readdir(dp)) != NULL) {
      if(strcmp(dirrp->d_name,".") == 0) continue;
      if(strcmp(dirrp->d_name,"..") == 0) continue;
      string tmp = path + dirrp->d_name;
      open_and_read(tmp,totle,flag,all);
    }
    if(all)
      cout<<"<==exit:==> "<<path<<endl;
    closedir(dp);
  }
  return 0;
}

int main(int argc,char*argv[])
{
  int option = 0;
  int totle = 0;
  string path;
  bool detail = false;
  bool all = false;
  while((option = getopt(argc,argv,"p:da")) != -1) {
    switch(option) {
    case 'p': {
                path = string(optarg,optarg+strlen(optarg));
                cout<<"dir path is "<<path<<endl;
                break;
              }
    case 'd': {
                detail = true;
                break;
              }
    case 'a': {
                all = true;
                break;
              }
    case '?': {
                cout<<"unknow"<<endl;
                break;
              }
    }
  }
  if(path.empty()) {
    cout<<"need input path"<<endl;
    cout<<"-p path -d detail -a all path"<<endl;
    _exit(0);
  }
  open_and_read(path,totle,detail,all);
  cout<<"totle:"<<"["<<totle<<"]"<<endl;
  cout<<"files:"<<"["<<files<<"]"<<endl;
  cout<<"average:"<<"["<<totle/files<<"]"<<endl;
  return 0;
}
