#nullable enable
using SimpleBankingCore.Core.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace SimpleBankingCore.Services.Interfaces
{
    public interface ICustomerService
    {
        Task<Customer> CreateCustomerAsync(string firstName, string lastName, string email);
        Task<Customer?> GetCustomerByIdAsync(int customerId);
        Task<Customer?> GetCustomerByEmailAsync(string email);
        Task<IEnumerable<Customer>> GetAllCustomersAsync();
    }
}
