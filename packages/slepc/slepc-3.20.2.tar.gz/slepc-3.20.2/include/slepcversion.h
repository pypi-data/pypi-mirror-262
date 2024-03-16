/*
   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   SLEPc - Scalable Library for Eigenvalue Problem Computations
   Copyright (c) 2002-, Universitat Politecnica de Valencia, Spain

   This file is part of SLEPc.
   SLEPc is distributed under a 2-clause BSD license (see LICENSE).
   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
*/

#ifndef SLEPCVERSION_H
#define SLEPCVERSION_H

#define SLEPC_VERSION_RELEASE    1
#define SLEPC_VERSION_MAJOR      3
#define SLEPC_VERSION_MINOR      20
#define SLEPC_VERSION_SUBMINOR   2
#define SLEPC_RELEASE_DATE       "September 29, 2023"
#define SLEPC_VERSION_DATE       "Mar 15, 2024"

#if !defined (SLEPC_VERSION_GIT)
#define SLEPC_VERSION_GIT        "v3.20.2"
#endif

#if !defined(SLEPC_VERSION_DATE_GIT)
#define SLEPC_VERSION_DATE_GIT   "2024-03-15 12:12:56 +0100"
#endif

#define SLEPC_VERSION_EQ(MAJOR,MINOR,SUBMINOR) \
 ((SLEPC_VERSION_MAJOR == (MAJOR)) &&       \
  (SLEPC_VERSION_MINOR == (MINOR)) &&       \
  (SLEPC_VERSION_SUBMINOR == (SUBMINOR)) && \
  (SLEPC_VERSION_RELEASE  == 1))

#define SLEPC_VERSION_ SLEPC_VERSION_EQ

#define SLEPC_VERSION_LT(MAJOR,MINOR,SUBMINOR)          \
  (SLEPC_VERSION_RELEASE == 1 &&                        \
   (SLEPC_VERSION_MAJOR < (MAJOR) ||                    \
    (SLEPC_VERSION_MAJOR == (MAJOR) &&                  \
     (SLEPC_VERSION_MINOR < (MINOR) ||                  \
      (SLEPC_VERSION_MINOR == (MINOR) &&                \
       (SLEPC_VERSION_SUBMINOR < (SUBMINOR)))))))

#define SLEPC_VERSION_LE(MAJOR,MINOR,SUBMINOR) \
  (SLEPC_VERSION_LT(MAJOR,MINOR,SUBMINOR) || \
   SLEPC_VERSION_EQ(MAJOR,MINOR,SUBMINOR))

#define SLEPC_VERSION_GT(MAJOR,MINOR,SUBMINOR) \
  (0 == SLEPC_VERSION_LE(MAJOR,MINOR,SUBMINOR))

#define SLEPC_VERSION_GE(MAJOR,MINOR,SUBMINOR) \
  (0 == SLEPC_VERSION_LT(MAJOR,MINOR,SUBMINOR))

#endif
