# The `iriuri` Python Package

_**WARNING:** This package is not yet ready for use!**_

The `iriuri` package will offer both generic and scheme-specific
IRI and URI parsing, validation, manipulation, and serialization.

It will also be able to serve as an Apache 2.0-licensed drop-in
replacement for at least the basic parsing/composing/resolving features
of the [GPL](https://www.gnu.org/licenses/gpl-3.0.en.html)'d
[`rfc3987`](https://pypi.org/project/rfc3987/) library (which I
highly recommend if you are able to comply with the conditions of GPL).

## Release timeline

This package is being developed by @handrews.  If you would like
for me to have more time for open source work, I would be grateful
for any [sponsorship](https://github.com/sponsors/handrews).

## Features

Initial functionality will target generic IRI/URI syntax, with
scheme-specific features for `http`, `https`, and `urn`, as well
as media-type-based fragment syntax for HTML, XML, YAML, JSON Schema,
and OpenAPI and `application/x-www-form-urlencoded` query strings
being prioritized next.

This libraries eventual goals include:

* Round-trip-safe parsing and serialization
    * correct handling of empty string vs null components
    * preservation of case for case-insensitive components
    * no unexpected automatic encoding or normalization
* Proper handling of base URIs/IRIs and URI/IRI-references
* Full compliance with the ABNF from appropriate standards, including:
    * RFC 3986 Uniform Resource Identifier (URI): Generic Syntax
    * RFC 3987 Internationalized Resource Identifiers (IRIs)
    * RFC 6874 Representing IPv6 Zone Identifiers in Address Literals and URIs
    * RFC 8141 Uniform Resource Names (URNs)
    * additional scheme-/query-/fragment-/urn-namespace-specific standards TBD
* Flexible options to balance performance and correctness
* Extensible parsing, validation, normalization, defaults, and comparisons
  for specific URI/IRI subsets
    * Scheme-specific for authority/query syntax
    * Query format-specific for query syntax
    * Media type-specific for fragment syntax
    * URN namespace-specific for namespace-specific string syntax
* A comprehensive test suite
    * Scheme-specific tests where relevant
    * Please file an issue if you know of public IRI test data!
    * CJK, right-to-left, vertical, and other display challenges
    * While not a display library, there is a gap in good IRI test data
    * Likely to include WHATWG's URL tests, although this library
      will comply with IETF standards; whether WHATWG support will
      ever be considered depends on the degree of divergence involved

