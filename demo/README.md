# Crypto Algorithm Detection Demo

This demo showcases the capabilities and limitations of the crypto algorithm detection tool. It includes several example files that demonstrate different scenarios:

## Example Files

### 1. game_characters.py
- **False Positive Example**
- Contains the word "fortuna" in a gaming context
- Tool detects it as a potential use of the Fortuna Random Number Generator
- Shows how keywords can be detected out of context

### 2. hash_utils.py
- **Commented Code Detection Example**
- Contains commented-out MD5 implementation
- Actually uses SHA-256 for hashing
- Tool detects both:
  - MD5 references in comments
  - Active SHA-256 implementation
- Demonstrates how the tool can flag deprecated algorithms even in comments

### 3. mixed_content.py
- **Mixed Usage Example**
- Contains both:
  - Real crypto usage (SHA-256)
  - False positives (Fortuna in game context)
  - Commented MD5 references
- Shows how the tool handles files with multiple contexts

### 4. crypto_examples.py
- **Direct Implementation Example**
- Contains actual crypto implementations
- Uses MD5, AES, and DES
- Represents a clear case of crypto usage

### 5. crypto_utils.js
- **Multiple Algorithm Example**
- Implements multiple crypto functions
- Uses Blowfish and SHA-256
- Shows detection across different programming languages

## Detection Results

The tool successfully detected:
1. All implemented crypto algorithms (SHA-256, Blowfish)
2. References in comments (MD5)
3. Keywords in non-crypto contexts (Fortuna)

This demonstrates both the tool's effectiveness in finding crypto implementations and its current limitations in distinguishing context.

## Key Takeaways

1. **Contextual Awareness**
   - The tool detects keywords regardless of context
   - Manual review may be needed to filter false positives

2. **Comment Detection**
   - Detects crypto references in comments
   - Useful for finding deprecated algorithm references
   - May require analysis to determine if the code is actually used

3. **Cross-Language Support**
   - Successfully detects crypto in both Python and JavaScript
   - Language-agnostic detection based on keywords

4. **False Positives**
   - Common words that match crypto algorithm names can trigger detection
   - Example: "Fortuna" in gaming context