dnl configure.ac
dnl
dnl Copyright 2012, 2013, 2014 Brandon Invergo <brandon@invergo.net>
dnl
dnl Copying and distribution of this file, with or without modification,
dnl are permitted in any medium without royalty provided the copyright
dnl notice and this notice are preserved.  This file is offered as-is,
dnl without any warranty.

AC_INIT([pyifbabel], [0.4], [brandon@invergo.net])
m4_include([m4/python.m4])
PC_INIT([2.5], [2.7.99])
AC_CONFIG_MACRO_DIR([m4])

AC_ARG_WITH([virtualenv],
	[AS_HELP_STRING([--with-virtualenv], [install to a Python virtualenv])],
	[],
	[with_virtualenv=no])
AS_IF([test "x$with_virtualenv" != xno],
	    AC_CHECK_PROGS([VIRTUALENV], [virtualenv virtualenv3 virtualenv2], [no])
	    AS_IF([test "x$VIRTUALENV" = xno],
	    [AC_MSG_FAILURE(
		[--with-virtualenv given but virtualenv could not be found])]),
	AC_SUBST([VIRTUALENV], [no]))
AC_ARG_VAR([VIRTUALENV_FLAGS], [flags to pass to the virtualenv command])

AC_PROG_MKDIR_P
AC_PROG_INSTALL	    

PC_PYTHON_SITE_PACKAGE_DIR
PC_PYTHON_EXEC_PACKAGE_DIR

AC_CONFIG_FILES([Makefile setup.py])
AC_OUTPUT
