import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;

/**
 * Parser for the Assembler
 * Upon construction receives a file and reads from it line-by-line.
 * IMPORTANT - REMEMBER TO CLOSE WHEN DONE USING, WE DON'T WANT TO LEAVE AN OPEN
 * STREAM!!
 */
public class Parser {
    private LineNumberReader reader;
    private String currentInstruction;
    private String nextInstruction;

    /**
     * @param sourceFile - The file that Parser reads from
     */
    public Parser(File sourceFile) {
        try {
            this.reader = new LineNumberReader(new FileReader(sourceFile));
            this.currentInstruction = null;
            this.nextInstruction = getNextLine();
            advance();

        } catch (Exception e) {
            System.out.println("Error while initializing Parser");
            e.printStackTrace();
        }
    }

    /**
     * @return Returns whether there are more files to read in the given file
     */
    public boolean hasMoreLines() {
        return currentInstruction != null;
    }

    /**
     * Advances the current instruction. Should only be used after insuring Parser
     * has more lines.
     * 
     * @return Whether the advance was successfull or not
     */
    public boolean advance() {
        try {
            this.currentInstruction = this.nextInstruction;
            this.nextInstruction = getNextLine();
            return true;
        } catch (Exception e) {
            System.out.println("Error while advancing the instruction");
            e.printStackTrace();
            return false;
        }
    }

    /**
     * Factory method to manage skipping of comments and whitespace
     * 
     * @return next line that isn't a comment or whitespace
     */
    private String getNextLine() {
        try {
            String nextLine;
            do {
                nextLine = reader.readLine();
                if (nextLine == null) {
                    return null;
                }
                nextLine = nextLine.trim();
            } while (nextLine.length() == 0 || nextLine.charAt(0) == '/');

            int commentIndex = nextLine.indexOf('/');
            int spaceIndex = nextLine.indexOf(" ");
            if (commentIndex != -1) {
                if (spaceIndex != -1) {
                    int stopIndex = (spaceIndex < commentIndex) ? spaceIndex : commentIndex;
                    nextLine = nextLine.substring(0, stopIndex);
                } else {
                    nextLine = nextLine.substring(0, commentIndex);
                }
            }
            return nextLine;
        } catch (IOException e) {
            System.out.println("Error while getting next line");
            e.printStackTrace();
            return null;
        }
    }

    /**
     * @return Returns the type of the current instruction as: X_INSTRUCTION (X =
     *         A/C/L)
     */
    public final String instructionType() {
        char first = this.currentInstruction.charAt(0);
        switch (first) {
            case '@':
                return "A_INSTRUCTION";
            case '(':
                return "L_INSTRUCTION";
        }
        return "C_INSTRUCTION";
    }

    /**
     * Returns the symbol of the current instruction. Should only be used if current
     * instruction is A or L
     * 
     * @return The Symbol as a String
     */
    public String symbol() {
        final String inst = instructionType();
        if (inst.equals("A_INSTRUCTION")) {
            return this.currentInstruction.substring(1);
        } else {
            return this.currentInstruction.substring(1, currentInstruction.length() - 1);
        }
    }

    /**
     * Returns the destination portion of the current C instruction. Should only be
     * used if current instruction is C.
     * 
     * @return The destination as a String. null if there isn't any.
     */
    public String dest() {
        int equalIndex = this.currentInstruction.indexOf('=');
        if (equalIndex == -1) {
            return null;
        } else {
            return this.currentInstruction.substring(0, equalIndex);
        }
    }

    /**
     * Returns the jump portion of the current C instruction. Should only be used if
     * current instruction is C.
     * 
     * @return The jump as a String. null if there isn't any.
     */
    public String jump() {
        int semicolon = this.currentInstruction.indexOf(';');
        if (semicolon == -1) {
            return null;
        } else {
            return this.currentInstruction.substring(semicolon + 1);
        }
    }

    /**
     * Returns the computation portion of the current C instruction. Should only be
     * used if current instruction is C.
     * 
     * @return The comp as a String.
     */
    public String comp() {
        int equalIndex = this.currentInstruction.indexOf('=');
        String modifiedInstruction = (equalIndex == -1) ? currentInstruction
                : currentInstruction.substring(equalIndex + 1);
        int semicolon = modifiedInstruction.indexOf(';');
        modifiedInstruction = (semicolon == -1) ? modifiedInstruction : modifiedInstruction.substring(0, semicolon);

        return modifiedInstruction;
    }

    /**
     * Closes the Parser. Important as to not leave the stream open.
     */
    public void close() {
        try {
            this.reader.close();
        } catch (IOException e) {
            System.out.println("Error while closing Parser");
            e.printStackTrace();
        }
    }

    /**
     * Main for testing.
     */
    public static void main(String[] args) {
        Parser parser = new Parser(new File("Prog.asm"));
        while (parser.hasMoreLines()) {
            String ins = parser.instructionType();
            System.out.println(ins);
            if (ins.equals("C_INSTRUCTION")) {
                System.out.println(parser.dest());
                System.out.println(parser.comp());
                System.out.println(parser.jump());
            } else
                System.out.println(parser.symbol());
            parser.advance();
        }
        parser.close();
    }
}
