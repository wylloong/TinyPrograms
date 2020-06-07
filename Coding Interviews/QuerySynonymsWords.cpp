#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

#include <boost/algorithm/string.hpp>

bool words_are_synonyms(
    const std::unordered_multimap<std::string, std::string> &synonym_words_hash,
    const std::string &first_str, const std::string &second_str) {
  // 同义词关系是双向的
  auto range = synonym_words_hash.equal_range(first_str);
  while (range.first != range.second) {

        std::cout << " " << range.first->second;
		if (second_str == range.first->second)
      return true;
    range.first++;
	}

	range = synonym_words_hash.equal_range(second_str);
  while (range.first != range.second) {

        std::cout << " " << range.first->second;
		if (first_str == range.first->second)
      return true;
    range.first++;
	}

  return false;
}

std::unordered_multimap<std::string, std::string> PreprocessSynonymWords(
    std::vector<std::pair<std::string, std::string>> synonym_words) {
  // 使用正确的数据结构来处理同义词.
  std::unordered_multimap<std::string, std::string> synonym_words_hash;
  for (std::pair<std::string, std::string> words : synonym_words) {
    synonym_words_hash.insert({words.first, words.second});
  }
  return synonym_words_hash;
}

// synonym_words: iterable of pairs of strings representing synonymous words
// queries: iterable of pairs of strings representing queries to be tested for
// synonymous-ness.
std::vector<bool>
synonym_queries(std::vector<std::pair<std::string, std::string>> synonym_words,
                std::vector<std::pair<std::string, std::string>> queries) {
  // 预处理同义词
  std::unordered_multimap<std::string, std::string> synonym_words_hash =
      PreprocessSynonymWords(synonym_words);

  std::vector<bool> output;
  for (std::pair<std::string, std::string> query : queries) {
    // Split the query strings.
    std::vector<std::string> query_results_1;
    boost::algorithm::split(query_results_1, query.first,
                            boost::is_any_of(" "));
    std::vector<std::string> query_results_2;
    boost::algorithm::split(query_results_2, query.second,
                            boost::is_any_of(" "));

    if (query_results_1.size() != query_results_2.size()) {
      output.push_back(false);
      continue;
    }

    bool result = true;
    for (int index = 0; index < query_results_1.size(); index++) {
      if (query_results_1.at(index) == query_results_2.at(index)) {
        continue;
      } else if (words_are_synonyms(synonym_words_hash,
                                    query_results_1.at(index),
                                    query_results_2.at(index))) {
        continue;
      }
      result = false;
      break;
    }
    output.push_back(result);
  }

  return output;
}

// ====================测试代码====================
void test(std::string testName,
          const std::vector<std::pair<std::string, std::string>> synonym_words,
          const std::vector<std::pair<std::string, std::string>> queries,
          const std::vector<bool> expected) {
  std::cout << testName << " begins: " << std::endl;

  std::vector<bool> query_results = synonym_queries(synonym_words, queries);
  if (query_results == expected) {
    printf("Passed.\n");
  } else {
    printf("FAILED.\n");
  }
}

void test1() {
  const std::vector<std::pair<std::string, std::string>> synonym_words = {
      {"rate", "ratings"}, {"approval", "popularity"}};
  const std::vector<std::pair<std::string, std::string>> queries = {
      {"obama approval rate", "obama popularity ratings"},
      {"obama approval rates", "obama popularity ratings"},
      {"obama approval rate", "popularity ratings obama"}};
  const std::vector<bool> expected = {true, false, false};
  test("Test1", synonym_words, queries, expected);
}

int main() {
  test1();
  return 0;
}
