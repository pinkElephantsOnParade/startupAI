//	cutmorph.c
//	字種に基づく形態素の切り出し
//	テキストから全角データのみ抽出して形態素を切り出します

#include <stdio.h>
#include <string.h>
#define MAX 65535*3 //192kバイトまで処理可能

/*テキストを読み込む*/
int getsource(char *s)
{
 int n=0 ;//文字数のカウンタ

 while((s[n++]=getchar())!=EOF) ;
 return n ;
}

 /*全角文字のみ取り出す*/
void getwidechar(char *t,char *s,int n)
{
 int in=0;//入力データのポインタ
 int out=0 ;//出力データのポインタ
 int d;
 while(in<n){
  d=(unsigned char)s[in] ;
  if(d & 0x80){//2バイト文字
    t[out++]=s[in++];
    t[out++]=s[in++];
    t[out++]=s[in++];
  }
  else ++in ;
 }
 t[out]='\0' ;//文字列の終端
}

/*漢字かそれ以外かの判別*/
int iskanji(char ch0, char ch1,char ch2)
{
 int d0, d1, d2;
 d0 = (unsigned char)ch0;
 d1 = (unsigned char)ch1;
 d2 = (unsigned char)ch2;
 if((d0 == 0xe4 && ( 0xb8 <= d1 && d1 <= 0xbf) && (0x80 <= d2 && d2 <= 0xbf))
  ||((0xe5 <= d0 && d0 <= 0xe9) && (0x80 <= d1 && d1 <= 0xbf) && (0x80 <= d2 && d2 <= 0xbf))
  ||(d0 == 0xef && d1 == 0xa4 && d2 == 0xa9)
  ||(d0 == 0xef && d1 == 0xa7 && d2 == 0x9c)
  ||(d0 == 0xef && d1 == 0xa8 && (0x8e <= d2 && d2 <= 0xad))
  ) return 1 ;
 else return 0 ;
}
/*カタカナかそれ以外かの判別*/
int iskatakana(char ch0, char ch1,char ch2)
{
 int d0,d1,d2 ;
 d0=(unsigned char)ch0 ;
 d1=(unsigned char)ch1 ;
 d2=(unsigned char)ch2 ;
 if((d0==0xe3 &&(d1==0x82)&&(0xa1 <= d2 && d2<= 0xbf))
  ||(d0==0xe3 &&(d1==0x83)&&(0x80 <= d2 && d2<= 0xb6))
  ||(d0==0xe3 && d1==0x83 && d2 == 0xbc)
  ) return 1 ;
 else return 0 ;
}
/*字種の設定*/
int typeset(char ch0, char ch1,char ch2)
{
 if(iskanji(ch0,ch1,ch2)) return 0 ;//漢字は０
 else if(iskatakana(ch0,ch1,ch2)) return 1 ;//カタカナは１
 else return 2 ;//その他は２
}
/*句読点の検出*/
int ispunct(char *ch)
{
 if((strncmp(ch,"．",3)==0)
  ||(strncmp(ch,"。",3)==0)
  ||(strncmp(ch,"，",3)==0)
  ||(strncmp(ch,"、",3)==0)
  ) return 1;//句読点なら１
  else return 0 ;
}
 /*形態素の切り出し*/
void outputmorph(char *target) 
{
 int i=0 ;
 int now,last;//漢字(0)・カタカナ(1)・その他(2)の別
 last=typeset(target[i], target[i+1],target[i+2]) ;
 while(target[i]!='\0'){
  if(ispunct(&(target[i]))==0){//句読点ではない
   /*文内の処理*/
   now = typeset(target[i], target[i+1],target[i+2]) ;
   if(now!=last) {//字種が変わっている
    putchar('\n') ;//区切りの改行を出力
    last=now ;
   }
    putchar(target[i++]) ;
    putchar(target[i++]) ;
    putchar(target[i++]) ;
  }
  else{//句読点
  /*文末などの処理*/
   putchar('\n') ;//区切りの改行を出力
   ++i;++i;++i;//句読点の読み飛ばし
   last=typeset(target[i], target[i+1],target[i+2]) ;   
  } 
 }
}

int main()
{
 char source[MAX] ;//入力データ
 char target[MAX] ;//全角データ
 int numchar ;//入力文字数

 /*テキストを読み込む*/
 numchar=getsource(source) ;

 /*全角文字のみ取り出す*/
 getwidechar(target,source,numchar) ;

 /*形態素の切り出し*/
 outputmorph(target) ;

 return 0 ;
}

