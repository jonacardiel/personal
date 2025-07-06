using System;

namespace SimpleBankingCore.Core.Exceptions
{
    // Custom exception for when an account has insufficient funds for a withdrawal/transfer
    public class InsufficientFundsException : Exception
    {
        public InsufficientFundsException() { }

        public InsufficientFundsException(string message) : base(message) { }

        public InsufficientFundsException(string message, Exception innerException)
            : base(message, innerException) { }
    }
}
