# Compression-HELIX

[![CI](https://github.com/kapildhinwa2010-dev/Compression-HELIX/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/Compression-HELIX/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/Compression-HELIX/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/Compression-HELIX/actions/workflows/codeql.yml)

Wave-lattice model store with adaptive bit-depth selection driven by an error tolerance.

## What it does

The base HybridStore encodes at one fixed bit depth. AdaptiveHybridStore
tries bit depths from 2 to 16 and keeps the smallest one whose
reconstruction error stays within your tolerance (relative RMSE against
the matrix standard deviation), then stores it in the same wave lattice.

    from compression_helix import AdaptiveHybridStore

    store = AdaptiveHybridStore(tolerance=0.05)
    stats = store.put_adaptive("layer0", W)
    print(stats)  # bits, ratio, relative_rmse
    print(store.compression_report())

## API

- HybridStore - the base fixed-bit-depth codec (unchanged from DNA-HELIX)
- AdaptiveHybridStore.put_adaptive(name, W, tolerance) - returns chosen stats
- AdaptiveHybridStore.compression_report() - per-model bits/ratio/error

## Honest results and limitations

- Relative RMSE is a global error metric: it can hide large local errors in
  small regions of the matrix.
- The candidate bit depths are fixed (2, 4, 8, 12, 16); the true optimum
  between two candidates is never tried.
- Tolerance is relative to matrix scale, so the same tolerance means
  different absolute errors for different matrices.

## Status

Part of the kapildhinwa2010-dev toolkit experiments. CI and CodeQL run on
every push to main. License: MIT.
