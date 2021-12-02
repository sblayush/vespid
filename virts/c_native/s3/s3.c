#pragma GCC push_options
#pragma GCC optimize ("O0")

int s3(int a){
    for(int i=0;i<a;i++){
        for (int j=0;j<a;j++){}
    }
  return a;
}

#pragma GCC pop_options