# URL Declustering Tool

This Python script processes a list of URLs to normalize and decluster them, ensuring that redundant, irrelevant, or duplicate URLs are filtered out and transformed into a consistent format. The tool is designed to streamline URL analysis and deduplication.

---

## Features

- **Protocol Normalization**: Converts all URLs to use the `https` protocol.
- **Path Cleanup**: Removes redundant slashes (`//`) and standardizes paths.
- **File Type Exclusion**: Filters out URLs pointing to static files such as images, JavaScript, CSS, etc.
- **Content Filtering**: Ignores blog posts, articles, and paginated content.
- **Dynamic Path Standardization**: Replaces numeric IDs and dates in paths with placeholders (e.g., `/cat/9/details.html` -> `/cat/id/details.html`).
- **Query Parameter Handling**:
  - Removes unnecessary tracking parameters (e.g., `utm_source`, `ref`, `session_id`).
  - Normalizes and standardizes specific query parameters like `id` and `page`.
  - Sorts query parameters alphabetically to ensure consistent ordering.
- **Fragment Removal**: Strips URL fragments (the `#` part).
- **Domain Normalization**: Converts domain names to lowercase.
- **Duplicate Elimination**: Ensures only unique URLs are included in the output.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/XiaomingX/url-declustering-tool.git
   cd url-declustering-tool
   ```
2. Ensure you have Python 3 installed:
   ```bash
   python3 --version
   ```
3. (Optional) Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

---

## Usage

1. Run the script with sample input:
   ```bash
   python3 decluster_urls.py
   ```
2. Modify the `input_urls` list in the `main()` function to test with custom URLs.

---

## Example

### Input
```plaintext
http://example.com/page.php?id=1
http://example.com/page.php?id=3&page=2
http://example.com/cat/9/details.html
http://example.com/2021/08/01/article-title
http://example.com/assets/background.jpg
http://example.com/?utm_source=google&utm_medium=cpc
```

### Output
```plaintext
https://example.com/page.php?id=id
https://example.com/cat/id/details.html
https://example.com/yyyy/mm/dd/
```

---

## How It Works

1. **Parse**: Each URL is parsed using `urllib.parse` for components such as scheme, domain, path, and query.
2. **Transform**:
   - Paths are cleaned and standardized.
   - Query parameters are normalized and irrelevant parameters are removed.
3. **Deduplicate**: Processed URLs are compared to a set of seen URLs to ensure uniqueness.
4. **Output**: A list of declustered URLs is returned.

---

## Customization

You can adjust the filtering logic or standardization rules by editing the corresponding sections of the `decluster_urls` function. For example:
- Add or remove static file extensions in the `endswith` check.
- Modify the list of unnecessary query parameters.
- Update regex patterns to match additional dynamic paths.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Feel free to submit issues or pull requests for feature enhancements or bug fixes. Contributions are welcome!