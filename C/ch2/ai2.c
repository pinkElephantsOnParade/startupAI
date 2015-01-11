//	ai2.c.c
//	2-gramの連鎖により文を作成する人工無能プログラムです
//	2-gramが格納されたファイル2gram.txtを用います


#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAXNO 100000 //2-gramの最大数
#define MAXLINE 256 //1行の最大バイト数
#define FILENAME "2gram.txt" //2-gramが格納されたファイル

/*2-gramファイルの読み込み*/
int read2gram(char db2gram[MAXNO][7])
{
 FILE *fp;
 char line[MAXLINE] ;
 int i=0 ;

 if((fp=fopen(FILENAME,"r"))==NULL){
  fprintf(stderr,"エラー　ファイル2gram.txtがありません\n");
  exit(1) ;
 }

 while(fgets(line,MAXLINE,fp)!=NULL){
  strncpy(db2gram[i],line,6) ;//全角2文字をコピー
  db2gram[i][6]='\0' ;
  ++i ;
 }
 return i ;//2-gramの個数を返す
}

/*開始文字が何回含まれるか数える*/
int findch(char *startch,char db2gram[MAXNO][7],int n) 
{
 int i ;
 int no=0 ;
 for(i=0;i<n;++i){
  if(strncmp(startch,db2gram[i],3)==0) ++ no ;
 }
 return no ;
}

/*num未満の乱数をセット*/
int setrnd(int num)
{
 int rndno ;
 while((rndno=(double)rand()/RAND_MAX*num)==num) ;
 return rndno ;

}

/*次の文字をn-gramによりランダムにセット*/
void setrndstr(char *startch,char db2gram[MAXNO][7],int n)
{
 int i ;
 int point ;
 
 point=setrnd(n) ;//n未満の乱数をセット
 for(i=0;i<n;++i){
  if(i==point){
   startch[0]=db2gram[i][3] ;
   startch[1]=db2gram[i][4] ;
   startch[2]=db2gram[i][5] ;
   startch[3]='\0' ;
   break ;
  }
 }  
}

/*次の文字をn-gramによりセット*/
void setnext(char *startch,char db2gram[MAXNO][7],int n,int num) 
{
 int i ;
 int no=0 ;
 int point ;
 
 point=setrnd(num) ;//num未満の乱数をセット
 for(i=0;i<n;++i){
  if(strncmp(startch,db2gram[i],3)==0) ++ no ;
  if(no==point){
   startch[0]=db2gram[i][3] ;
   startch[1]=db2gram[i][4] ;
   startch[2]=db2gram[i][5] ;
   startch[3]='\0' ;
   break ;
   break ;
  }
 }  
}

/*文の生成*/
void generates(char *startch,char db2gram[MAXNO][7],int n)
{
 int i,num ;
 
  /*開始文字を出力する*/
  putchar(startch[0]) ; putchar(startch[1]); putchar(startch[2]);
  /*句点が出るまで繰り返し*/

 do{
  /*開始文字が何回含まれるか数える*/
  num=findch(startch,db2gram,n) ;
  /*その中からランダムに文字列を選ぶ*/
  if(num!=0)
   setnext(startch,db2gram,n,num) ;
  else
   setrndstr(startch,db2gram,n) ;
  /*文字を出力する*/
  putchar(startch[0]) ; putchar(startch[1]); putchar(startch[2]);
 }while((strncmp(startch,"．",3)!=0)&&(strncmp(startch,"。",3)!=0)) ;
 printf("\n") ;
}

int main()
{
 char line[MAXLINE] ;//入力バッファ
 char db2gram[MAXNO][7] ;//2gramのデータベース
 int n ;//2-gramの個数
 char startch[MAXLINE];//開始文字
 
 
 /*乱数の初期化*/
 srand(65535) ;
 /*2-gramファイルの読み込み*/
 n=read2gram(db2gram) ;
 int num = 0; 
 /*オープニングメッセージ*/
 printf("さくら：メッセージをどうぞ\n");
 printf("あなた：");
 /*会話しましょう*/
 while(fgets(line,MAXLINE,stdin)!=NULL ){

  if(strlen(line) < 3 && line[0] == 'q'){
    break;
  }

  printf("さくら：");
  num = setrnd((strlen(line)-1)/3)*3;
  strncpy(startch,&(line[num]),3) ;
  generates(startch,db2gram,n) ;
  printf("あなた：");
 }
 /*エンディングメッセージ*/
 printf("さくら：ばいば～い\n");
 return 0 ;
}
