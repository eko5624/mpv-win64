From 7aba58f8ca31624c3a8e73fe07c80a4d526c436e Mon Sep 17 00:00:00 2001
From: Christopher Degawa <ccom@randomderp.com>
Date: Sat, 31 Oct 2020 19:05:40 +0000
Subject: [PATCH] libm_wrapper: define __CRT__NO_INLINE before math.h

it seems *zimg_x_expf and some others pick up the inline function
pointer and labels expf etc as defined instead of linking to a system's
library
---
 src/zimg/common/libm_wrapper.cpp | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)

diff --git a/src/zimg/common/libm_wrapper.cpp b/src/zimg/common/libm_wrapper.cpp
index d92e08c..01f8a15 100644
--- a/src/zimg/common/libm_wrapper.cpp
+++ b/src/zimg/common/libm_wrapper.cpp
@@ -1,5 +1,6 @@
-#include <math.h>
 #include "libm_wrapper.h"
+#define __CRT__NO_INLINE 1
+#include <math.h>
 
 float (*zimg_x_expf)(float) = expf;
 float (*zimg_x_logf)(float) = logf;
-- 
2.25.1
