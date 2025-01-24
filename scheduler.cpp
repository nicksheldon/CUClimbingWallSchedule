#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int main() {
    // Vectors to hold the data
    vector<string> names;
    vector<vector<char>> slots;
    vector<char> allSlots = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R'};

    // Open the CSV file
    ifstream file("responses.csv");
    if (!file.is_open()) {
        cerr << "Could not open the file!" << endl;
        return 1;
    }


    string line;

    // Read file line by line
    while (getline(file, line)) {

        stringstream ss(line);
        string token;

        // Ignore the first value (use getline to move over the first token)
        getline(ss, token, ',');

        // Read the second value (name) and add it to the names vector
        getline(ss, token, ',');
        names.push_back(token);

        // Read the third value (list of characters)
        getline(ss, token);

        // Remove the quotes
        if (token.front() == '"') {
            token = token.substr(1, token.length() - 1);
        }

        // Create a vector to store characters
        vector<char> charList;

        // Remove spaces from the string if any
        token.erase(remove(token.begin(), token.end(), ' '), token.end());

        // Split the string by commas and push each character into the vector
        stringstream charStream(token);
        while (getline(charStream, token, ',')) {
            charList.push_back(token[0]); // Push the first character
        }

        // Push the vector of characters into the slots vector
        slots.push_back(charList);
    }

    // Close the file
    file.close();

    // DONE WITH FILE READING ********************************************************************

    // Sort names and slots by the length of the corresponding slot vectors
    vector<pair<string, vector<char>>> pairedData;

    // Pair each name with its corresponding slot
    for (size_t i = 0; i < names.size(); ++i) {
        pairedData.push_back({names[i], slots[i]});
    }

    // Sort the paired data based on the length of the vector (slot)
    sort(pairedData.begin(), pairedData.end(), 
        [](const pair<string, vector<char>>& a, const pair<string, vector<char>>& b) {
            return a.second.size() < b.second.size();
        });

    // Unpack the sorted data back into names and slots
    names.clear();
    slots.clear();
    for (const auto& pair : pairedData) {
        names.push_back(pair.first);
        slots.push_back(pair.second);
    }

    vector<tuple<char,char,char>> slotsWithNames;

    for (int i = 0; i < allSlots.size(); i++) {
        slotsWithNames.push_back({allSlots[i], '\0', '\0'});
    }

    // DONE WITH SORTING **************************************************************************

    for (int i = 0; i < names.size(); i++) {
        cout << names[i] << ": ";
        for (int j = 0; j < slots[i].size(); j++) {
            cout << slots[i][j] << ", ";
        }
        cout << endl;
    }

    return 0;
}
