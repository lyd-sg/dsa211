# Retired GitHub Actions workflows

These YAML files were moved here from `.github/workflows/` as part of retiring the old project versions. **GitHub Actions does not register workflows outside `.github/workflows/`**, so they are not automatically or manually dispatchable as live workflows from this archive.

They remain available for historical verification only, with the original contents and path assumptions preserved:

- `build-prd-v3.yml`: v3.0
- `build-prd-v3-1.yml`: v3.1
- `build-prd-v3-2.yml`: v3.2
- `build-prd-v3-3.yml`: v3.3
- `build-prd-v3-4.yml`: v3.4
- `validate-notebook.yml`: early revised notebook
- [verify-prd-v3-5.yml](verify-prd-v3-5.yml): v3.5 historical presentation audit
- [build-prd-v3-6.yml](build-prd-v3-6.yml): v3.6 historical full execution

**Active workflow:** [verify-prd-v3-7.yml](../../.github/workflows/verify-prd-v3-7.yml) verifies the executed current notebook and saved evidence **without refitting models**. Historical CI definitions are not runnable from their relocated paths without explicit, carefully reviewed adaptation, and should not be reactivated casually.
