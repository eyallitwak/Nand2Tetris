import java.io.File;

public class Code {
    /**
     * @param dest - Symbolic destination of C instruction.
     * @return Binary representation of parameter (null if empty).
     */
    public static String dest(String dest) {
        if (dest != null) {
            StringBuilder builder = new StringBuilder();
            char destA = (dest.indexOf('A') != -1) ? '1' : '0';
            char destD = (dest.indexOf('D') != -1) ? '1' : '0';
            char destM = (dest.indexOf('M') != -1) ? '1' : '0';
            builder.append(destA);
            builder.append(destD);
            builder.append(destM);
            return builder.toString();
        } else
            return "000";
    }

    /**
     * @param jump - Symbolic jump portion of C instruction.
     * @return Binary representation of parameter (null if empty).
     */
    public static String jump(String jump) {
        if (jump != null) {
            switch (jump) {
                case "JGT":
                    return "001";
                case "JEQ":
                    return "010";
                case "JGE":
                    return "011";
                case "JLT":
                    return "100";
                case "JNE":
                    return "101";
                case "JLE":
                    return "110";
                case "JMP":
                    return "111";
                default:
                    System.out.println("Error while converting jump to binary, illegal jump");
                    return null;
            }
        } else
            return "000";

    }

    /**
     * @param comp - Symbolic comp portion of C instruction.
     * @return Binary representation of parameter.
     */
    public static String comp(String comp) {
        switch (comp) {
            case "0":
                return "0101010";
            case "1":
                return "0111111";
            case "-1":
                return "0111010";
            case "D":
                return "0001100";
            case "A":
                return "0110000";
            case "!D":
                return "0001101";
            case "!A":
                return "0110001";
            case "-D":
                return "0001111";
            case "-A":
                return "0110011";
            case "D+1":
                return "0011111";
            case "A+1":
                return "0110111";
            case "D-1":
                return "0001110";
            case "A-1":
                return "0110010";
            case "D+A":
                return "0000010";
            case "D-A":
                return "0010011";
            case "A-D":
                return "0000111";
            case "D&A":
                return "0000000";
            case "D|A":
                return "0010101";
            case "M":
                return "1110000";
            case "!M":
                return "1110001";
            case "-M":
                return "1110011";
            case "M+1":
                return "1110111";
            case "M-1":
                return "1110010";
            case "D+M":
                return "1000010";
            case "D-M":
                return "1010011";
            case "M-D":
                return "1000111";
            case "D&M":
                return "1000000";
            case "D|M":
                return "1010101";
        }
        System.out.println("Error while parsing comp. null Returned null");
        return null;
    }

    public static void main(String[] args) {
        Parser parser = new Parser(new File("Prog.asm"));
        System.out.println("DEST: " + dest(parser.dest()));
        System.out.println("COMP: " + comp(parser.comp()));
        System.out.println("JUMP: " + jump(parser.jump()));
    }
}
