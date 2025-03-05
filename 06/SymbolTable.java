import java.util.HashMap;

public class SymbolTable extends HashMap<String, Integer> {
    private static final int DATA_UPPER_LIMIT = 16384;

    // keeps track for variables' addresses
    private int symbolsAdded = 16;

    public SymbolTable() {
        super();
        addEntry("R0", 0);
        addEntry("R1", 1);
        addEntry("R2", 2);
        addEntry("R3", 3);
        addEntry("R4", 4);
        addEntry("R5", 5);
        addEntry("R6", 6);
        addEntry("R7", 7);
        addEntry("R8", 8);
        addEntry("R9", 9);
        addEntry("R10", 10);
        addEntry("R11", 11);
        addEntry("R12", 12);
        addEntry("R13", 13);
        addEntry("R14", 14);
        addEntry("R15", 15);
        addEntry("SCREEN", 16384);
        addEntry("KBD", 24576);
        addEntry("SP", 0);
        addEntry("LCL", 1);
        addEntry("ARG", 2);
        addEntry("THIS", 3);
        addEntry("THAT", 4);
    }

    public void addEntry(String symbol, int address) {
        this.put(symbol, address);
    }

    public void addEntry(String symbol) {
        if (symbolsAdded + 1 == DATA_UPPER_LIMIT) {
            throw new RuntimeException();
        } else {
            addEntry(symbol, symbolsAdded);
            symbolsAdded++;
        }
    }

    public boolean contains(String symbol) {
        return this.containsKey(symbol);
    }

    public int getAddress(String symbol) {
        return this.get(symbol);
    }
}
